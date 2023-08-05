import torch
from torch import nn
import numpy as np
import pandas as pd
from sklearn.mixture import BayesianGaussianMixture, GaussianMixture
from sklearn.utils.testing import ignore_warnings
from sklearn.exceptions import ConvergenceWarning
from scipy.stats import gaussian_kde
from .constants import CATEGORICAL, CONTINUOUS, DATE


class Transformer:

    @staticmethod
    def get_metadata(data, categorical_columns=tuple(), date_columns=tuple()):
        meta = []

        df = pd.DataFrame(data)
        for index in df:
            column = df[index]

            if index in categorical_columns:
                mapper = column.value_counts().index.tolist()
                meta.append({
                    "name": index,
                    "type": CATEGORICAL,
                    "size": len(mapper),
                    "i2s": mapper,
                    'dtype': data[index].dtype,
                })
            elif index in date_columns:
                meta.append({
                    "name": index,
                    "type": DATE,
                    "min": column.min(),
                    'max': column.max(),
                    'dtype': data[index].dtype,
                })
            else:
                meta.append({
                    "name": index,
                    "type": CONTINUOUS,
                    "min": column.min(),
                    "max": column.max(),
                    'n_decimals': str(column[0])[::-1].find('.'),
                    'dtype': data[index].dtype,
                })

        return meta

    def fit(self, data, categorical_columns=tuple()):
        raise NotImplementedError

    def transform(self, data: pd.DataFrame):
        raise NotImplementedError

    def inverse_transform(self, data: pd.DataFrame):
        raise NotImplementedError

    def fit_transform(self, data: pd.DataFrame, categorical_columns=None):
        self.fit(data, categorical_columns=categorical_columns)
        return self.transform(data)


class GeneralTransformer(Transformer):
    """Continuous and discrete columns are normalized to [0, 1].
    Discrete columns are converted to a one-hot vector.
    """

    def __init__(self, act='sigmoid'):
        self.act = act
        self.meta = None
        self.output_dim = None

    def fit(self, data, categorical_columns=tuple()):
        self.meta = self.get_metadata(data, categorical_columns)
        self.output_dim = 0
        for info in self.meta:
            if info['type'] in [CONTINUOUS]:
                self.output_dim += 1
            else:
                self.output_dim += info['size']

    def transform(self, data):
        data_t = []
        self.output_info = []
        for id_, info in enumerate(self.meta):
            col = data[:, id_]
            if info['type'] == CONTINUOUS:
                col = (col - (info['min'])) / (info['max'] - info['min'])
                if self.act == 'tanh':
                    col = col * 2 - 1
                data_t.append(col.reshape([-1, 1]))
                self.output_info.append((1, self.act))

            elif info['type'] == CATEGORICAL:
                col = col / info['size']
                if self.act == 'tanh':
                    col = col * 2 - 1
                data_t.append(col.reshape([-1, 1]))
                self.output_info.append((1, self.act))

            else:
                col_t = np.zeros([len(data), info['size']])
                col_t[np.arange(len(data)), col.astype('int32')] = 1
                data_t.append(col_t)
                self.output_info.append((info['size'], 'softmax'))

        return np.concatenate(data_t, axis=1)

    def inverse_transform(self, data):
        data_t = np.zeros([len(data), len(self.meta)])

        data = data.copy()
        for id_, info in enumerate(self.meta):
            if info['type'] == CONTINUOUS:
                current = data[:, 0]
                data = data[:, 1:]

                if self.act == 'tanh':
                    current = (current + 1) / 2

                current = np.clip(current, 0, 1)
                data_t[:, id_] = current * (info['max'] - info['min']) + info['min']

            elif info['type'] == CATEGORICAL:
                current = data[:, 0]
                data = data[:, 1:]

                if self.act == 'tanh':
                    current = (current + 1) / 2

                current = current * info['size']
                current = np.round(current).clip(0, info['size'] - 1)
                data_t[:, id_] = current
            else:
                current = data[:, :info['size']]
                data = data[:, info['size']:]
                data_t[:, id_] = np.argmax(current, axis=1)

        return data_t


class GMMTransformer(Transformer):
    """
    Continuous columns are modeled with a GMM.
        and then normalized to a scalor [0, 1] and a n_cluster dimensional vector.

    Discrete columns are converted to a one-hot vector.
    """

    def __init__(self, n_clusters=5, n_stds=4):
        self.meta = None
        self.n_clusters = n_clusters
        self.n_stds = n_stds

    @ignore_warnings(category=ConvergenceWarning)
    def fit(self, data: pd.DataFrame, categorical_columns=tuple()):
        self.meta = self.get_metadata(data, categorical_columns)
        model = []

        self.output_info = []
        self.output_dim = 0
        for id_, info in enumerate(self.meta):
            if info['type'] == CONTINUOUS:
                gm = GaussianMixture(self.n_clusters)
                gm.fit(data.iloc[:, id_].values.reshape([-1, 1]))
                model.append(gm)
                self.output_info += [(1, 'tanh'), (self.n_clusters, 'softmax')]
                self.output_dim += 1 + self.n_clusters
            else:
                model.append(None)
                self.output_info += [(info['size'], 'softmax')]
                self.output_dim += info['size']

        self.model = model

    def transform(self, data):
        values = []
        for id_, info in enumerate(self.meta):
            current = data.iloc[:, id_].values
            if info['type'] == CONTINUOUS:
                current = current.reshape([-1, 1])

                means = self.model[id_].means_.reshape((1, self.n_clusters))
                stds = np.sqrt(self.model[id_].covariances_).reshape((1, self.n_clusters))
                features = (current - means) / (self.n_stds * stds)

                probs = self.model[id_].predict_proba(current.reshape([-1, 1]))
                argmax = np.argmax(probs, axis=1)
                idx = np.arange((len(features)))
                features = features[idx, argmax].reshape([-1, 1])

                features = np.clip(features, -.99, .99)

                values += [features, probs]
            else:
                col_t = np.zeros([len(data), info['size']])
                col_t[np.arange(len(data)), current.astype('int32')] = 1
                values.append(col_t)

        return np.concatenate(values, axis=1)

    def inverse_transform(self, data, sigmas):
        data_t = np.zeros([len(data), len(self.meta)])

        st = 0
        for id_, info in enumerate(self.meta):
            if info['type'] == CONTINUOUS:
                u = data[:, st]
                v = data[:, st + 1:st + 1 + self.n_clusters]
                if sigmas is not None:
                    sig = sigmas[st]
                    u = np.random.normal(u, sig)

                u = np.clip(u, -1, 1)
                st += 1 + self.n_clusters
                means = self.model[id_].means_.reshape([-1])
                stds = np.sqrt(self.model[id_].covariances_).reshape([-1])
                p_argmax = np.argmax(v, axis=1)
                std_t = stds[p_argmax]
                mean_t = means[p_argmax]
                tmp = u * self.n_stds * std_t + mean_t
                data_t[:, id_] = tmp

            else:
                current = data[:, st:st + info['size']]
                st += info['size']
                data_t[:, id_] = np.argmax(current, axis=1)

        return data_t


class BGMTransformer(Transformer):
    """Model continuous columns with a BayesianGMM and normalized to a scalar [-1, 1] and a vector.

    Discrete columns are converted to a one-hot vector.
    """

    def __init__(self, n_clusters=10, eps=0.005, n_stds=4):
        """n_cluster is the upper bound of modes."""
        self.meta = None
        self.n_clusters = n_clusters
        self.eps = eps
        self.n_stds = n_stds

    @ignore_warnings(category=ConvergenceWarning)
    def fit(self, data, categorical_columns=tuple()):
        self.meta = self.get_metadata(data, categorical_columns)
        model = []

        self.output_info = []
        self.output_dim = 0
        self.components = []
        for id_, info in enumerate(self.meta):
            if info['type'] == CONTINUOUS:
                gm = BayesianGaussianMixture(
                    self.n_clusters,
                    weight_concentration_prior_type='dirichlet_process',
                    weight_concentration_prior=0.001,
                    n_init=1)
                gm.fit(data.iloc[:, id_].values.reshape([-1, 1]))
                model.append(gm)
                comp = gm.weights_ > self.eps
                self.components.append(comp)

                self.output_info += [(1, 'tanh'), (np.sum(comp), 'softmax')]
                self.output_dim += 1 + np.sum(comp)
            else:
                model.append(None)
                self.components.append(None)
                self.output_info += [(info['size'], 'softmax')]
                self.output_dim += info['size']

        self.model = model

    def transform(self, data):
        values = []
        for id_, info in enumerate(self.meta):
            current = data.iloc[:, id_].values
            if info['type'] == CONTINUOUS:
                current = current.reshape([-1, 1])

                means = self.model[id_].means_.reshape((1, self.n_clusters))
                stds = np.sqrt(self.model[id_].covariances_).reshape((1, self.n_clusters))
                features = (current - means) / (self.n_stds * stds)

                probs = self.model[id_].predict_proba(current.reshape([-1, 1]))

                n_opts = sum(self.components[id_])
                features = features[:, self.components[id_]]
                probs = probs[:, self.components[id_]]

                opt_sel = np.zeros(len(data), dtype='int')
                for i in range(len(data)):
                    pp = probs[i] + 1e-6
                    pp = pp / sum(pp)
                    opt_sel[i] = np.random.choice(np.arange(n_opts), p=pp)

                idx = np.arange((len(features)))
                features = features[idx, opt_sel].reshape([-1, 1])
                features = np.clip(features, -.99, .99)

                probs_onehot = np.zeros_like(probs)
                probs_onehot[np.arange(len(probs)), opt_sel] = 1
                values += [features, probs_onehot]
            else:
                col_t = np.zeros([len(data), info['size']])
                col_t[np.arange(len(data)), current.astype('int32')] = 1
                values.append(col_t)

        return np.concatenate(values, axis=1)

    def inverse_transform(self, data, sigmas):
        data_t = np.zeros([len(data), len(self.meta)])

        st = 0
        for id_, info in enumerate(self.meta):
            if info['type'] == CONTINUOUS:
                u = data[:, st]
                v = data[:, st + 1:st + 1 + np.sum(self.components[id_])]

                if sigmas is not None:
                    sig = sigmas[st]
                    u = np.random.normal(u, sig)

                u = np.clip(u, -1, 1)
                v_t = np.ones((data.shape[0], self.n_clusters)) * -100
                v_t[:, self.components[id_]] = v
                v = v_t
                st += 1 + np.sum(self.components[id_])
                means = self.model[id_].means_.reshape([-1])
                stds = np.sqrt(self.model[id_].covariances_).reshape([-1])
                p_argmax = np.argmax(v, axis=1)
                std_t = stds[p_argmax]
                mean_t = means[p_argmax]
                tmp = u * self.n_stds * std_t + mean_t
                data_t[:, id_] = tmp

            else:
                current = data[:, st:st + info['size']]
                st += info['size']
                data_t[:, id_] = np.argmax(current, axis=1)

        return data_t


class Tokenizer(Transformer):
    def __init__(self, categorical_columns=None, date_columns=None):
        self.categorical_columns = () if categorical_columns is None else categorical_columns
        self.date_columns = () if date_columns is None else date_columns
        self.mapping = {}
        self.reverse_mapping = {}
        self.columns = None

    def fit(self, data: pd.DataFrame):
        self.meta = self.get_metadata(data, self.categorical_columns, self.date_columns)
        for id_, info in enumerate(self.meta):
            if info['type'] in [CATEGORICAL]:
                col = info['name']
                y, uniques = pd.factorize(data[col].astype('object'))
                self.mapping[col] = {n: i for i, n in enumerate(uniques)}
                self.reverse_mapping[col] = uniques
            else:
                continue

    def transform(self, data: pd.DataFrame):
        self.columns = data.columns
        numeric_data = data.copy()
        for id_, info in enumerate(self.meta):
            if info['type'] in [CATEGORICAL]:
                col = info['name']
                numeric_data[col] = [self.mapping[col][i] for i in data[col]]
        return numeric_data

    def inverse_transform(self, numeric_data):
        numeric_data = pd.DataFrame(numeric_data, columns=self.columns)
        data = numeric_data.copy()
        for id_, info in enumerate(self.meta):
            col = info['name']
            if info['type'] in [CATEGORICAL]:
                data[col] = [self.reverse_mapping[col][int(i)] for i in numeric_data[col]]
            else:
                pass
                data[col] = data[col].clip(info['min'], info['max'])
            data[col] = data[col].astype(info['dtype'])
        return data

    @staticmethod
    def get_categorical_columns(data: pd.DataFrame):
        categorical_columns = []
        categorical_columns += data.select_dtypes(include=['object', 'category']).columns.tolist()
        return tuple(categorical_columns)


class InputCleaner(Transformer):
    """
    This class has three main functions.
     1. Substitute NaNs in categorical columns with a placeholder value.
     2. Temporarily removing constant columns. We don't need neural networks to handle them.
     3. Handle broken continuous columns. With broken continuous columns, we mean columns that contain continuous data
        but also have missing data. This creates a complex situation with regards to sampling data.
    """

    def __init__(self, sampling_method='kde'):
        """
        :param sampling_method: Method to sample data for the broken continuous data. Must be in [`kde`, `gaussian`].
        """
        self.constant_columns_meta = None
        self.categorical_columns = None
        self.broken_continuous_columns_meta = None
        self.sampling_method = sampling_method

    def fit(self, df, categorical_columns=None, missing_pct=0.0):
        self.constant_columns_meta = []
        self.categorical_columns = []
        self.broken_continuous_columns_meta = []
        self.missing_pct = missing_pct
        self.categorical_columns = Tokenizer.get_categorical_columns(df) if categorical_columns is None else categorical_columns


        # Remove constant columns and save values
        _constant_columns_idx = df.loc[:, (df != df.iloc[0]).any() == False].columns.tolist()
        for column in _constant_columns_idx:
            self.constant_columns_meta.append({
                'column_label': column,
                'value': df.loc[0, column],
            })

        # Drop continues columns with too much missing values.
        _broken_continuous_columns_idx = df.loc[:, df.isna().sum() / len(df) > missing_pct].columns.tolist()
        percentage_missing = df.isna().sum() / len(df)
        self.broken_continuous_columns_meta = []
        for column in _broken_continuous_columns_idx:
            self.broken_continuous_columns_meta.append({
                'column_label': column,
                'mean': df.loc[:, column].mean(),
                'std': df.loc[:, column].std(),
                'pct_missing': percentage_missing[column],
                'dtype': np.int64 if df.loc[~df[column].isna(), column].apply(lambda x: x.is_integer()).all() else df.loc[:, column].dtype,
                'model':  gaussian_kde(df.loc[~df[column].isna(), column], bw_method='silverman') if self.sampling_method == 'kde' else None
            })

    def transform(self, df, drop_threshold=0.05):
        """
        Apply transformations according to parameters learned from `fit` method to `df`.
        :param df: DataFrame containing non-transformed data
        :return: DataFrame with transformed features
        """
        df = df.copy()

        # Drop constant columns
        print('Removing constant columns: ', [a['column_label'] for a in self.constant_columns_meta])
        df = df.drop([a['column_label'] for a in self.constant_columns_meta], axis=1)

        # Fill empty cells for discrete columns.
        print('Filling categorical columns: ', list(self.categorical_columns))
        df.loc[:, self.categorical_columns] = df.loc[:, self.categorical_columns].fillna('[NAN]')

        # Drop continuous columns with broken values
        print('Removing broken continuous columns: ', [a['column_label'] for a in self.broken_continuous_columns_meta if a['pct_missing'] > drop_threshold])
        df = df.drop([a['column_label'] for a in self.broken_continuous_columns_meta if a['pct_missing'] > drop_threshold], axis=1)

        # Drop rows with missing values in columns with percentage lower than `drop_threshold`
        _drop_rows_columns = [a['column_label'] for a in self.broken_continuous_columns_meta if drop_threshold > a['pct_missing'] > 0.0]
        _drop_rows_idxs = df[df[_drop_rows_columns].isna().any(axis=1)].index.tolist()
        df = df.drop(_drop_rows_idxs, axis=0)
        return df

    def inverse_transform(self, df, ):
        """
        Apply inverse transformation on `df` according to fitted parameters.
        :param df: DataFrame containing transformed data
        :return: df with inverse transformed features.
        """
        df = df.copy()

        # Reset constant value columns
        for constant_column in self.constant_columns_meta:
            df[constant_column['column_label']] = constant_column['value']

        # Remove NAN placeholder
        df.replace(to_replace='[NAN]', value={a: None for a in self.categorical_columns})

        # Fill broken continuous columns with value from a sampled distribution.
        for continuous_column in self.broken_continuous_columns_meta:
            if self.sampling_method == 'kde':
                df[continuous_column['column_label']] = continuous_column['model'].resample(size=(len(df))).reshape(-1).astype(continuous_column['dtype'])
            elif self.sampling_method == 'gaussian':
                df[continuous_column['column_label']] = np.random.normal(loc=continuous_column['mean'], scale=continuous_column['std'], size=(len(df))).astype(continuous_column['dtype'])
            else:
                raise ValueError('`self.continuous_sampling` should be in [`gaussian`, `kde`].')
            drop_idxs = np.random.choice(np.arange(len(df)), replace=False, size=int(continuous_column['pct_missing']*len(df)))
            df.loc[drop_idxs, continuous_column['column_label']] = None
        return df
