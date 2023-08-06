# -*- coding: utf-8 -*-
#
# This file is part of s4d.
#
# s4d is a python package for speaker diarization.
# Home page: http://www-lium.univ-lemans.fr/s4d/
#
# s4d is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# s4d is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with s4d.  If not, see <http://www.gnu.org/licenses/>.


"""
Copyright 2014-2020 Anthony Larcher
"""

import os
import sys
import numpy
import random
import h5py
import torch
import torch.nn as nn
from torch import optim
from torch.utils.data import Dataset
import logging

from sidekit.nnet.vad_rnn import BLSTM

__license__ = "LGPL"
__author__ = "Anthony Larcher"
__copyright__ = "Copyright 2015-2020 Anthony Larcher"
__maintainer__ = "Anthony Larcher"
__email__ = "anthony.larcher@univ-lemans.fr"
__status__ = "Production"
__docformat__ = 'reS'




class PreNet(nn.Module):
    def __init(self,
               sample_rate=16000,
               windows_duration=0.2,
               frame_shift=0.01):
        super(PreNet, self).__init__()

        windows_length = int(sample_rate * windows_duration)
        if windows_length % 2:
            windows_length += 1
        stride_0 = int(sample_rate * frame_shift)

        self.conv0 = torch.nn.Conv1d(1, 64, windows_length, stride=stride_0, dilation=1)
        self.conv1 = torch.nn.Conv1d(64, 64, 3, dilation=1)
        self.conv2 = torch.nn.Conv1d(64, 64, 3, dilation=1)

        self.norm0 = torch.nn.BatchNorm1d(64)
        self.norm1 = torch.nn.BatchNorm1d(64)
        self.norm2 = torch.nn.BatchNorm1d(64)

        self.activation = torch.nn.LeakyReLU(0.2)


    def forward(self, input):

        x = self.norm0(self.activation(self.conv0(input)))
        x = self.norm1(self.activation(self.conv1(x)))
        output = self.norm2(self.activation(self.conv2(x)))

        return output




class BLSTM(nn.Module):
    """
    Bi LSTM model used for voice activity detection or speaker turn detection
    """
    def __init__(self,
                 input_size,
                 lstm_1,
                 lstm_2,
                 linear_1,
                 linear_2,
                 output_size=1):
        """

        :param input_size:
        :param lstm_1:
        :param lstm_2:
        :param linear_1:
        :param linear_2:
        :param output_size:
        """
        super(BLSTM, self).__init__()

        self.lstm_1 = nn.LSTM(input_size, lstm_1 // 2, bidirectional=True, batch_first=True)
        self.lstm_2 = nn.LSTM(lstm_1, lstm_2 // 2, bidirectional=True, batch_first=True)
        self.linear_1 = nn.Linear(lstm_2, linear_1)
        self.linear_2 = nn.Linear(linear_1, linear_2)
        self.output = nn.Linear(linear_2, output_size)
        self.hidden = None

    def forward(self, inputs):
        """

        :param inputs:
        :return:
        """
        if self.hidden is None:
            hidden_1, hidden_2 = None, None
        else:
            hidden_1, hidden_2 = self.hidden
        tmp, hidden_1 = self.lstm_1(inputs, hidden_1)
        x, hidden_2 = self.lstm_2(tmp, hidden_2)
        self.hidden = (hidden_1, hidden_2)
        x = torch.tanh(self.linear_1(x))
        x = torch.tanh(self.linear_2(x))
        x = torch.sigmoid(self.output(x))
        return x

class SeqToSeq(nn.Module):

    def __init__(self):
        self.model = BLSTM(input_size=1,
                           lstm_1=64,
                           lstm_2=40,
                           linear_1=40,
                           linear_2=10)





class VAD_RNN:
    """
    A VAD_RNN is meant to use a PyTorch RNN model for Speech Activity Detection
    """

    def __init__(self, input_size, duration, step, batch_size, model_file_name=None):
        """
        :param input_size: size of the input features
        :param duration: duration in seconds of each batch of features
        :param step: duration in seconds of each step between two batches
        :param batch_size: batch size
        :param model_file_name: optional pytorch model to load If None, the default model is used.
        The default model is made of two BLSTM layers of dimension 64 and 40
        followed by two linear layers of dimension 40 and 10.
        """
        self.input_size = input_size
        self.duration = int(duration * 100)
        self.step = int(step * 100)
        self.batch_size = batch_size

        if model_file_name is None:
            self.model = BLSTM(input_size=self.input_size,
                               lstm_1=64,
                               lstm_2=40,
                               linear_1=40,
                               linear_2=10)
        else:
            self.model.load_state_dict(torch.load(model_file_name))

        self.model.to(device)

    def _fit_batch(self, optimizer, criterion, x, y):
        """
        Internal method used to train the network
        :param optimizer:
        :param criterion:
        :param X:
        :param Y:

        :return: loss of current batch
        """
        x = x.to(device)
        y = y.to(device)
        self.model.hidden = None
        optimizer.zero_grad()
        lstm_out = self.model(x)
        loss = criterion(lstm_out, y)
        loss.backward()
        optimizer.step()
        return float(loss.data)

    def get_scores(self, show, features_server, score_file_format=''):
        """
        Computes the scores for one show from the output of the network
        :param show: the show to extract
        :param features_server: a sidekit FeaturesServer object
        :param score_file_format: optional, used to save or load a score file

        :return: scores of the show, as an array of 0..1
        """

        if score_file_format == '':
            score_fn = ''
        else:
            score_fn = score_file_format.format(show)
        if os.path.exists(score_fn):
            print("Warning: loading existing scores")
            return numpy.load(score_fn)

        features, _ = features_server.load(show)

        x = []
        for i in range(0, len(features) - self.duration, self.step):
            x.append(features[i:i + self.duration])
            if i + self.step > len(features) - self.duration:
                pad_size = self.batch_size - len(x)
                pad = [[[0] * self.input_size] * self.duration] * pad_size
                x += pad

        x = torch.Tensor(x).to(device)
        self.model.hidden = None
        x = self.model(x)

        o = numpy.asarray(x.squeeze(2).tolist())
        scores = numpy.zeros((len(o) * self.step + self.duration - self.step))
        w = numpy.zeros(scores.shape)
        start = 0
        for i, out in enumerate(o):
            scores[start:start + self.duration] += out
            w[start:start + self.duration] += 1
            start += self.step

        scores = scores / w
        scores = scores[:len(features)]
        if score_fn != '':
            numpy.save(score_fn, scores)
        return scores

    def train_network(self,
                      nb_epochs,
                      training_set,
                      model_file_format):
        """
        Trains the network

        :param nb_epochs: number of epochs to do
        :param training_set: Dataset object to feed the training algorithm as keys. The start and stop are in
        centiseconds.
        :param model_file_format: file format to save the model. The format uses the current epoch
        """
        criterion = nn.BCELoss()
        optimizer = optim.RMSprop(self.model.parameters())

        losses = []
        for epoch in range(nb_epochs):
            it = 1
            losses.append([])
            for batch_idx, (X, Y) in enumerate(training_set):
                batch_loss = self._fit_batch(optimizer, criterion, X, Y)
                losses[epoch].append(batch_loss)
                logging.critical("Epoch {}/{}, loss {:.5f}".format(
                    epoch + 1, nb_epochs, numpy.mean(losses[epoch])))
                it += 1
            torch.save(self.model.state_dict(), model_file_format.format(epoch + 1))

    def vad_blstm(self, show, features_server, onset=0.8, offset=0.95, scores_fn=''):
        """
        Get the VAD labels for one show
        :param show: show to generate the SAD from
        :param features_server: a sidekit FeaturesServer object
        :param onset: score threshold above which a segment should start
        :param offset: score threshold under which a segment should stop
        :param scores_fn: optional file name to save the scores
        """
        scores = self.get_scores(show, features_server, scores_fn)

        label = numpy.zeros(len(scores))

        start = 0
        segment = False
        for i, s in enumerate(scores):
            if not segment and s > onset:  # speech segment begins
                start = i
                segment = True
            if segment and s < offset:  # speech segment ends
                segment = False
                label[start:i] = 1
        if segment:
            label[start:i] = 1

        return label

    def write_vad(self, show_list, features_server, onset, offset, vad_file_format, scores_file_format=''):
        """
        Generates the SAD segment files from the trained model

        :param show_list: list of shows to generate the SAD from
        :param features_server: a sidekit FeaturesServer object
        :param onset: score threshold above which a segment will start
        :param offset: score threshold below which a segment will stop
        :param vad_file_format: file format for the segments
        :param scores_file_format: optional, used to save scores files
        """
        for show in sorted(show_list):
            scores = self.get_scores(show, features_server, scores_file_format)

            sad = []

            start = 0
            segment = False
            for i, s in enumerate(scores):
                if not segment and s > onset:
                    start = i
                    segment = True
                if segment and s < offset:
                    segment = False
                    sad.append([show, start, i])
            if segment or len(sad) == 0:
                sad.append([show, start, i])
            with open(vad_file_format.format(show), 'w') as f:
                for l in sad:
                    f.write("{} 1 {} {} U U U speech\n".format(l[0], l[1], l[2]))


