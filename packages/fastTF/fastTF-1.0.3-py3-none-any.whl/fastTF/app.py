import pandas as pd
import tensorflow as tf


class tfRecordWriter:
    def __init__(self, dataset):
        """
        Initializing the assumption_data types with the ones in the Pandas Dataframe.
        Make everything easier by splitting the columns with the proper datatypes.
        :param: dataset A pandas dataset to convert to a tfrecords

        >>> data = pd.read_csv('diabetes.csv')
        >>> test = tfRecordWriter(data)
        >>> test.int_features
        ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'Age', 'Outcome']

        """
        if not isinstance(dataset, pd.DataFrame):
            raise TypeError("Must be a pandas dataframe unlike " + str(type(dataset)))
        self.assumption_dtypes = dict(zip(dataset.columns, map(str, dataset.dtypes)))
        self._easier_features()
        self.dataset = dataset

    def get_example_spec(self):
        """
        Get example spec of the dataset to help load the file with extension *.tfrecords.
        :return: feature_spec A feature spec corresponding to the pandas dataset

        >>> data = pd.read_csv('diabetes.csv')
        >>> test = tfRecordWriter(data)
        >>> test.get_example_spec()
        {'Pregnancies': FixedLenFeature(shape=(), dtype=tf.int64, default_value=None),
        'Glucose': FixedLenFeature(shape=(), dtype=tf.int64, default_value=None),
        'BloodPressure': FixedLenFeature(shape=(), dtype=tf.int64, default_value=None),
        'SkinThickness': FixedLenFeature(shape=(), dtype=tf.int64, default_value=None),
        'Insulin': FixedLenFeature(shape=(), dtype=tf.int64, default_value=None),
        'Age': FixedLenFeature(shape=(), dtype=tf.int64, default_value=None),
        'Outcome': FixedLenFeature(shape=(), dtype=tf.int64, default_value=None),
        'BMI': FixedLenFeature(shape=(), dtype=tf.float32, default_value=None),
        'DiabetesPedigreeFunction': FixedLenFeature(shape=(), dtype=tf.float32, default_value=None)}

        """
        feature_spec = {}
        for int_feature in self.int_features:
            feature_spec[int_feature] = tf.io.FixedLenFeature((), tf.int64)
        for string_features in self.string_features:
            feature_spec[string_features] = tf.io.FixedLenFeature((), tf.string)
        for float_feature in self.float_features:
            feature_spec[float_feature] = tf.io.FixedLenFeature((), tf.float32)
        return feature_spec

    def _easier_features(self):
        """
        Make lists of each dtype.
        Supported dtypes: int64,int32,object,float64,float32

        """
        self.int_features = []
        self.float_features = []
        self.string_features = []
        for column, dtype in self.assumption_dtypes.items():
            if dtype == "int64" or dtype == "int32":
                self.int_features.append(column)
            elif dtype == "object":
                self.string_features.append(column)
            elif dtype == "float64" or dtype == "float32":
                self.float_features.append(column)

    def _create_example(self, data):
        """
            Convert dataset_row into a Tensorflow Example.
            Supported Features: String, Float,Int

            :param dataset_row: a pandas dataset row
            :return: A tensorflow example from the pandas dataset row
            >>> data = pd.read_csv('diabetes.csv')
            >>> test = tfRecordWriter(data)
            >>> test._create_example(data.iloc[0])
            features {
      feature {
        key: "Age"
        value {
          int64_list {
            value: 50
          }
        }
      }
      feature {
        key: "BMI"
        value {
          float_list {
            value: 33.599998474121094
          }
        }
      }
      feature {
        key: "BloodPressure"
        value {
          int64_list {
            value: 72
          }
        }
      }
      feature {
        key: "DiabetesPedigreeFunction"
        value {
          float_list {
            value: 0.6269999742507935
          }
        }
      }
      feature {
        key: "Glucose"
        value {
          int64_list {
            value: 148
          }
        }
      }
      feature {
        key: "Insulin"
        value {
          int64_list {
            value: 0
          }
        }
      }
      feature {
        key: "Outcome"
        value {
          int64_list {
            value: 1
          }
        }
      }
      feature {
        key: "Pregnancies"
        value {
          int64_list {
            value: 6
          }
        }
      }
      feature {
        key: "SkinThickness"
        value {
          int64_list {
            value: 35
          }
        }
      }
    }

        """
        feature_row = {}
        self._get_string_features(feature_row, data)
        self._get_float_features(feature_row, data)
        self._get_int_features(feature_row, data)
        feature_object = tf.train.Features(feature=feature_row)
        return tf.train.Example(features=feature_object)

    def _get_string_features(self, feature_row, data):
        """
        Get String tf.train.Features of a Pandas Dataframe Row and put it into a dictionary

        :param feature_row: A dictionary to put the tf.Train.Feature in
        :param data: A row of a pandas dataframe

        """
        if self.string_features:
            for feature in self.string_features:
                try:
                    string_list = data[feature].encode()
                    byte_list = tf.train.BytesList(value=[string_list])
                    feature_row[feature] = tf.train.Feature(bytes_list=byte_list)
                except BaseException as e:
                    raise ValueError(
                        "Please use a string object instead of a " + str(type(data[feature])) + "\nFull Error : " + str(
                            e))

    def _get_float_features(self, feature_row, data):
        """
            Get Float tf.train.Features of a Pandas Dataframe Row and put it into a dictionary

            :param feature_row: A dictionary to put the tf.Train.Feature in
            :param data: A row of a pandas dataframe

        """
        if self.float_features:
            for feature in self.float_features:
                try:
                    float_list = tf.train.FloatList(value=[data[feature]])
                    feature_row[feature] = tf.train.Feature(float_list=float_list)
                except BaseException as e:
                    raise ValueError("Please use a float instead of a ",
                                     type(data[feature]) + "\nFull Error : " + str(e))

    def get_feature_types(self):
        """
        Get previously assumed features

        :return: int_features Assumed Integer Features
        :return: float_features Assumed Float Features
        :return: string_features Assumed String Features

        >>> data = pd.read_csv('diabetes.csv')
        >>> test = tfRecordWriter(data)
        >>> test.get_feature_types()
        (['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'Age', 'Outcome'], ['BMI', 'DiabetesPedigreeFunction'], [])
        """
        return self.int_features, self.float_features, self.string_features

    def _get_int_features(self, feature_row, data):
        """
            Get Integer tf.train.Features of a Pandas Dataframe Row and put it into a dictionary

            :param feature_row: A dictionary to put the tf.Train.Feature in
            :param data: A row of a pandas dataframe
        """
        if self.int_features:
            for feature in self.int_features:
                try:
                    int_list = tf.train.Int64List(value=[int(data[feature])])
                    feature_row[feature] = tf.train.Feature(int64_list=int_list)
                except BaseException as e:
                    raise ValueError("Please use a long or an int instead of a ",
                                     type(data[feature]) + "\nFull Error : " + str(e))

    def write(self, path):
        """
        Loop through the dataset and make examples and write it to a tfrecords file and close the file.
        :param: path a path for the tfrecords to be stored in

        """
        writer = tf.io.TFRecordWriter(path)
        for row_num in range(len(self.dataset)):
            example = self._create_example(self.dataset.iloc[row_num])
            writer.write(example.SerializeToString())
        writer.close()


