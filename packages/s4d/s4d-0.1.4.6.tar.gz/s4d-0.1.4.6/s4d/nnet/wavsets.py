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

__license__ = "LGPL"
__author__ = "Anthony Larcher"
__copyright__ = "Copyright 2015-2020 Anthony Larcher and Sylvain Meignier"
__maintainer__ = "Anthony Larcher"
__email__ = "anthony.larcher@univ-lemans.fr"
__status__ = "Production"
__docformat__ = 'reStructuredText'

import numpy
import scipy
import sidekit
import torch

from ..diar import Diar
from pathlib import Path
from torch.utils.data import Dataset


def framing(sig, win_size, win_shift=1, context=(0, 0), pad='zeros'):
    """
    :param sig: input signal, can be mono or multi dimensional
    :param win_size: size of the window in term of samples
    :param win_shift: shift of the sliding window in terme of samples
    :param context: tuple of left and right context
    :param pad: can be zeros or edge
    """
    dsize = sig.dtype.itemsize
    if sig.ndim == 1:
        sig = sig[:, numpy.newaxis]
    # Manage padding
    c = (context, ) + (sig.ndim - 1) * ((0, 0), )
    _win_size = win_size + sum(context)
    shape = (int((sig.shape[0] - win_size) / win_shift) + 1, 1, _win_size, sig.shape[1])
    strides = tuple(map(lambda x: x * dsize, [win_shift * sig.shape[1], 1, sig.shape[1], 1]))
    return numpy.lib.stride_tricks.as_strided(sig,
                                           shape=shape,
                                           strides=strides).squeeze()

def load_wav_segment(wav_file_name, idx, duration, seg_shift, framerate=16000):
    """

    :param wav_file_name:
    :param idx:
    :param duration:
    :param seg_shift:
    :param framerate:
    :return:
    """
    # Load waveform
    signal = sidekit.frontend.io.read_audio(wav_file_name, framerate)[0]
    tmp = framing(signal,
                  int(framerate * duration),
                  win_shift=int(framerate * seg_shift),
                  context=(0, 0),
                  pad='zeros')
    return tmp[idx]


def mdtm_to_label(mdtm_filename,
              show_duration,
              framerate):
    """

    :param show:
    :param show_duration:
    :param allies_dir:
    :param mode:
    :param duration:
    :param start:
    :param framerate:
    :param filter_type:
    :param collar_duration:
    :return:
    """
    diarization = Diar.read_mdtm(mdtm_filename)
    diarization.sort(['show', 'start'])

    # Create a dictionary of speakers
    speaker_set = diarization.unique('cluster')
    speaker_dict = {}
    for idx, spk in enumerate(speaker_set):
        speaker_dict[spk] = idx

    # Create the empty labels
    label = numpy.zeros(show_duration, dtype=int)

    # Fill the labels with spk_idx
    for segment in diarization:
        start = int(segment['start']) * framerate // 100
        stop = int(segment['stop']) * framerate // 100
        spk_idx = speaker_dict[segment['cluster']]
        label[start:stop] = spk_idx

    return label


def get_segment_label(label, seg_idx, mode, duration, framerate, seg_shift, collar_duration, filter_type="gate"):

    # Create labels with Diracs at every speaker change detection
    spk_change = numpy.zeros(label.shape, dtype=int)
    spk_change[:-1] = label[:-1] ^ label[1:]
    spk_change = numpy.not_equal(spk_change, numpy.zeros(label.shape, dtype=int))

    # depending of the mode, generates the labels and select the segments
    if mode == "vad":
        output_label = (label > 0.5).astype(numpy.long)

    elif mode == "spk_turn":
        # Apply convolution to replace diracs by a chosen shape (gate or triangle)
        filter_sample = collar_duration * framerate * 2 + 1
        conv_filt = numpy.ones(filter_sample)
        if filter_type == "triangle":
            conv_filt = scipy.signal.triang(filter_sample)
        output_label = numpy.convolve(conv_filt, spk_change, mode='same')

    elif mode == "overlap":
        raise NotImplementedError()

    else:
        raise ValueError("mode parameter must be 'vad', 'spk_turn' or 'overlap'")

    # Create segments with overlap
    segment_label = framing(output_label,
                  int(framerate * duration),
                  win_shift=int(framerate * seg_shift),
                  context=(0, 0),
                  pad='zeros')

    return segment_label[seg_idx]


class AlliesSet(Dataset):
    """
    Object creates a dataset for
    """
    def __init__(self,
                 allies_dir,
                 mode,
                 duration=2.,
                 seg_shift=0.25,
                 filter_type="gate",
                 collar_duration=0.1,
                 framerate=16000):
        """
        Create batches of wavform samples for deep neural network training


        :param allies_dir: the root directory of ALLIES data
        :param mode:  can be "vad", "spk_turn", "overlap"
        :param duration: duration of the segments in seconds
        :param seg_shift: shift to generate overlaping segments
        :param filter_type:
        :param collar_duration:
        """
        self.framerate = framerate
        self.show_duration = {}
        self.segments = []
        self.duration  = duration
        self.seg_shift = seg_shift
        self.input_dir = allies_dir
        self.mode = mode
        self. filter_type = filter_type
        self.collar_duration = collar_duration
        self.wav_name_format = allies_dir + '/wav/{}.wav'
        self.mdtm_name_format = allies_dir + '/mdtm/{}.mdtm'

        # load the list of training file names
        training_file_list = [str(f).split("/")[-1].split('.')[
                                  0] for f in list(Path(allies_dir + "/wav/").rglob("*.[wW][aA][vV]"))
                              ]

        for show in training_file_list:

            # Load waveform
            signal = sidekit.frontend.io.read_audio(self.wav_name_format.format(show), self.framerate)[0]

            # Get speaker labels from MDTM
            label = mdtm_to_label(self.mdtm_name_format.format(show), signal.shape, self.framerate)

            # Create labels with Diracs at every speaker change detection
            spk_change = numpy.zeros(signal.shape, dtype=int)
            spk_change[:-1] = label[:-1] ^ label[1:]
            spk_change = numpy.not_equal(spk_change, numpy.zeros(signal.shape, dtype=int))

            # Create short segments with overlap
            tmp = framing(spk_change,
                          int(self.framerate * duration),
                          win_shift=int(self.framerate * seg_shift),
                          context=(0, 0),
                          pad='zeros')

            # Select only segments with at least a speaker change
            keep_seg = numpy.not_equal(tmp.sum(1), 0)
            keep_idx = numpy.argwhere(keep_seg.squeeze()).squeeze()

            for idx in keep_idx:
                self.segments.append((show, idx))

            self.len = len(self.segments)

    def __getitem__(self, index):
        show, idx = self.segments[index]

        data, total_duration = load_wav_segment(self.wav_name_format.format(show),
                                        idx, self.duration, self.seg_shift, framerate=self.framerate)

        tmp_label = mdtm_to_label(self.mdtm_name_format.format(show), total_duration, self.framerate)
        label = get_segment_label(tmp_label, idx, self.mode, self.duration, self.framerate,
                                  self.seg_shift, self.collar_duration, filter_type=self.filter_type)
        return torch.from_numpy(data).type(torch.FloatTensor), torch.from_numpy(label.astype('long'))

    def __len__(self):
        return self.len
