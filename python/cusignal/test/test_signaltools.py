# Copyright (c) 2019-2020, NVIDIA CORPORATION.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
import cupy as cp
from cusignal.test.utils import array_equal
import cusignal
import numpy as np
from scipy import signal


@pytest.mark.parametrize('num_samps', [2**14])
@pytest.mark.parametrize('resample_num_samps', [2**12, 2**16])
@pytest.mark.parametrize('window', [('kaiser', 0.5)])
def test_resample(num_samps, resample_num_samps, window):
    cpu_time = np.linspace(0, 10, num_samps, endpoint=False)
    cpu_sig = np.cos(-cpu_time ** 2 / 6.0)
    gpu_sig = cp.asarray(cpu_sig)

    cpu_resample = signal.resample(cpu_sig, resample_num_samps, window=window)
    gpu_resample = cp.asnumpy(
        cusignal.resample(gpu_sig, resample_num_samps, window=window)
    )

    assert array_equal(cpu_resample, gpu_resample)


@pytest.mark.parametrize('num_samps', [2**14])
@pytest.mark.parametrize('up', [2, 3, 7])
@pytest.mark.parametrize('down', [1, 2, 9])
@pytest.mark.parametrize('window', [('kaiser', 0.5)])
def test_resample_poly(num_samps, up, down, window):
    cpu_time = np.linspace(0, 10, num_samps, endpoint=False)
    cpu_sig = np.cos(-cpu_time ** 2 / 6.0)
    gpu_sig = cp.asarray(cpu_sig)

    cpu_resample = signal.resample_poly(cpu_sig, up, down, window=window)
    gpu_resample = cp.asnumpy(
        cusignal.resample_poly(gpu_sig, up, down, window=window)
    )

    assert array_equal(cpu_resample, gpu_resample)


@pytest.mark.parametrize('num_samps', [2**15])
@pytest.mark.parametrize('f1', [0.1, 0.15])
@pytest.mark.parametrize('f2', [0.2, 0.4])
def test_firwin(num_samps, f1, f2):
    cpu_window = signal.firwin(num_samps, [f1, f2], pass_zero=False)
    gpu_window = cp.asnumpy(
        cusignal.firwin(num_samps, [f1, f2], pass_zero=False)
    )
    assert array_equal(cpu_window, gpu_window)


@pytest.mark.parametrize('num_samps', [2**15])
@pytest.mark.parametrize('num_taps', [128, 2**8, 2**15])
def test_correlate(num_samps, num_taps, mode='same'):
    cpu_sig = np.random.rand(num_samps)
    gpu_sig = cp.asarray(cpu_sig)

    cpu_corr = signal.correlate(cpu_sig, np.ones(num_taps), mode=mode)
    gpu_corr = cp.asnumpy(
        cusignal.correlate(gpu_sig, cp.ones(num_taps), mode=mode)
    )
    assert array_equal(cpu_corr, gpu_corr)


@pytest.mark.parametrize('num_samps', [2**15])
@pytest.mark.parametrize('num_taps', [128, 2**8, 2**15])
def test_convolve(num_samps, num_taps, mode='same'):
    cpu_sig = np.random.rand(num_samps)
    cpu_win = signal.windows.hann(num_taps)

    gpu_sig = cp.asarray(cpu_sig)
    gpu_win = cusignal.windows.hann(num_taps)

    cpu_conv = signal.convolve(cpu_sig, cpu_win, mode=mode)
    gpu_conv = cp.asnumpy(cusignal.convolve(gpu_sig, gpu_win, mode=mode))
    assert array_equal(cpu_conv, gpu_conv)


@pytest.mark.parametrize('num_samps', [2**15])
def test_fftconvolve(num_samps, mode='full'):
    cpu_sig = np.random.rand(num_samps)
    gpu_sig = cp.asarray(cpu_sig)

    cpu_autocorr = signal.fftconvolve(cpu_sig, cpu_sig[::-1], mode=mode)
    gpu_autocorr = cp.asnumpy(
        cusignal.fftconvolve(gpu_sig, gpu_sig[::-1], mode=mode)
    )
    assert array_equal(cpu_autocorr, gpu_autocorr)


@pytest.mark.parametrize('num_samps', [2**15, 2**24])
def test_wiener(num_samps):
    cpu_sig = np.random.rand(num_samps)
    gpu_sig = cp.asarray(cpu_sig)

    cpu_wfilt = signal.wiener(cpu_sig)
    gpu_wfilt = cp.asnumpy(cusignal.wiener(gpu_sig))
    assert array_equal(cpu_wfilt, gpu_wfilt)


@pytest.mark.parametrize('num_samps', [2**15])
def test_hilbert(num_samps):
    cpu_sig = np.random.rand(num_samps)
    gpu_sig = cp.asarray(cpu_sig)

    cpu_hilbert = signal.hilbert(cpu_sig)
    gpu_hilbert = cp.asnumpy(cusignal.hilbert(gpu_sig))
    assert array_equal(cpu_hilbert, gpu_hilbert)


@pytest.mark.parametrize('num_samps', [2**8])
def test_hilbert2(num_samps):
    cpu_sig = np.random.rand(num_samps, num_samps)
    gpu_sig = cp.asarray(cpu_sig)

    cpu_hilbert2 = signal.hilbert2(cpu_sig)
    gpu_hilbert2 = cp.asnumpy(cusignal.hilbert2(gpu_sig))
    assert array_equal(cpu_hilbert2, gpu_hilbert2)


@pytest.mark.parametrize('num_samps', [2**8])
@pytest.mark.parametrize('num_taps', [5, 100])
@pytest.mark.parametrize('boundary', ['symm'])
@pytest.mark.parametrize('mode', ['same'])
def test_convolve2d(num_samps, num_taps, boundary, mode):
    cpu_sig = np.random.rand(num_samps, num_samps)
    cpu_filt = np.random.rand(num_taps, num_taps)
    gpu_sig = cp.asarray(cpu_sig)
    gpu_filt = cp.asarray(cpu_filt)

    cpu_convolve2d = signal.convolve2d(
        cpu_sig, cpu_filt, boundary=boundary, mode=mode
    )
    gpu_convolve2d = cp.asnumpy(
        cusignal.convolve2d(gpu_sig, gpu_filt, boundary=boundary, mode=mode)
    )
    assert array_equal(cpu_convolve2d, gpu_convolve2d)


@pytest.mark.parametrize('num_samps', [2**8])
@pytest.mark.parametrize('num_taps', [5, 100])
@pytest.mark.parametrize('boundary', ['symm'])
@pytest.mark.parametrize('mode', ['same'])
def test_correlate2d(num_samps, num_taps, boundary, mode):
    cpu_sig = np.random.rand(num_samps, num_samps)
    cpu_filt = np.random.rand(num_taps, num_taps)
    gpu_sig = cp.asarray(cpu_sig)
    gpu_filt = cp.asarray(cpu_filt)

    cpu_correlate2d = signal.correlate2d(
        cpu_sig, cpu_filt, boundary=boundary, mode=mode
    )
    gpu_correlate2d = cp.asnumpy(
        cusignal.correlate2d(gpu_sig, gpu_filt, boundary=boundary, mode=mode)
    )
    assert array_equal(cpu_correlate2d, gpu_correlate2d)

# Currently pure python to check correct implementation and build out GPU support
@pytest.mark.parametrize('order', [4, 16, 32])
@pytest.mark.parametrize('num_samps_x', [2**5, 2**10, 2**12, 2**15])
@pytest.mark.parametrize('mode', ['real'])
def test_lfilter(order, num_samps_x, mode):
    if mode == 'real':
        cpu_b, cpu_a = signal.butter(order, 0.5)
        #gpu_b = cp.asarray(cpu_b)
        #gpu_a = cp.asarray(cpu_a)
        cpu_x = np.random.randn(num_samps_x)
        #gpu_x = cp.asarray(cpu_x)

    cpu_lfilter = signal.lfilter(cpu_b, cpu_a, cpu_x)
    gpu_lfilter = cusignal.lfilter(cpu_b, cpu_a, cpu_x)

    #lfilter sometimes returns NaNs for ill-formed sizes, so remove
    cpu_lfilter = cpu_lfilter[~np.isnan(cpu_lfilter)]
    gpu_lfilter = gpu_lfilter[~np.isnan(cpu_lfilter)]

    assert array_equal(cpu_lfilter, gpu_lfilter)