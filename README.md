## Getting Started
### Dependencies

You'll need the following packages in order to run the test script:

* [Keras](https://keras.io/#installation "Install Keras")
* [Tensorflow](https://www.tensorflow.org/versions/r0.12/get_started/os_setup "Download and Install Tensorflow")
* Numpy
* Matplotlib
* [Graphviz executables](http://www.graphviz.org/Download.php "Download Graphviz") (Optional) - add these to `PATH`
* [PyDot](https://pypi.python.org/pypi/pydot "or use 'pip install pydot'") (Optional)


### Training Datasets
Grab the full collection of CSV files from [here](https://goo.gl/iHmPs9
"Google Drive download link"), unzip and place the `histrorical` directory in the project directory under /data

### Running the test
In terminal, run `python tensorflowtest.py --help` to view a list of all available command line options:
    
    usage: tensorflowtest.py [-h] [-p P] [-i I] [--epochs EPOCHS]
                         [--seqlen SEQLEN] [--split SPLIT]
                         [--infeatures [INFEATURES [INFEATURES ...]]]
                         [--outfeatures [OUTFEATURES [OUTFEATURES ...]]]
                         [--load LOAD]

    optional arguments:
      -h, --help            show this help message and exit
      -p P                  Currency pair
      -i I                  Sampling interval
      --epochs EPOCHS       Number of training epochs
      --seqlen SEQLEN       Length of sequences to train LSTM on
      --split SPLIT         Fraction by which to split testing and training data
                            (<1)
      --infeatures [INFEATURES [INFEATURES ...]]
                            Input features to use (can use multiple)
      --outfeatures [OUTFEATURES [OUTFEATURES ...]]
                            Output features to predict
      --load LOAD           Whether to load model from saved file on disk
      
Run `python tensorflowtest.py -p BTC_ETH -i 120 --seqlen 51 --log-INFO` to get the following output:
    
    Using TensorFlow backend.
    Model successfully built.
    Compilation Time: 0.02942986543944854
    C:\ProgramData\Anaconda3\lib\site-packages\keras\models.py:848: UserWarning: The `nb_epoch` argument in `fit` has been renamed `epochs`.
      warnings.warn('The `nb_epoch` argument in `fit` '
    Train on 7282 samples, validate on 810 samples
    Epoch 1/1
    7282/7282 [==============================] - 6s - loss: 1.2871e-04 - val_loss: 5.3770e-04
    INFO:__main__:training took 8.796115636825562 seconds
    C:\ProgramData\Anaconda3\lib\site-packages\matplotlib\backend_bases.py:2453: MatplotlibDeprecationWarning: Using default event loop until function specific to this GUI is implemented
      warnings.warn(str, mplDeprecation)
    