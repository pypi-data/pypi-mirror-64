from ml_platform_client.server.server import run_app
from ml_platform_client.config import GlobalConfig
from ml_platform_client.dispatcher import register

# from model.dispatcher import register, set_config
# from server.server import run_app
# from config import GlobalConfig

from test.algorithms import MyAlgorithm

minio_host = '172.16.100.247:9000'
minio_access_key = '24WTCKX23M0MRI6BA72Y'
minio_secret_key = '6mxoQMf1Lha2q1H3fp3fjNHEZRJJ7LvbC5k3+CQX'
minio_secure = False

if __name__ == '__main__':
    config = GlobalConfig()
    config.minio_host = minio_host
    config.minio_access_key = minio_access_key
    config.minio_secret_key = minio_secret_key
    config.minio_secure = minio_secure

    register('myalg', MyAlgorithm)
    # set_config(config)
    run_app(port=10001)
