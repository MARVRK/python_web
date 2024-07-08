import unittest
import os
from src.conf.config import Settings
class TestSettings(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.environ['SECRET_KEY'] = 'your_secret_key'
        os.environ['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///./test.db'
        os.environ['SMTP_HOST'] = 'smtp.example.com'
        os.environ['SMTP_PORT'] = '587'
        os.environ['SMTP_USERNAME'] = 'user@example.com'
        os.environ['SMTP_PASSWORD'] = 'password'
        os.environ['MAIL_FROM'] = 'noreply@example.com'
        os.environ['CLOUDINARY_CLOUD_NAME'] = 'cloud_name'
        os.environ['CLOUDINARY_API_KEY'] = '1234567890'
        os.environ['CLOUDINARY_API_SECRET'] = 'your_api_secret'
        os.environ['REDIS_HOST'] = 'localhost'
        os.environ['REDIS_PORT'] = '6379'
        os.environ['ALGORITHM'] = 'HS256'

    def test_settings(self):
        config = Settings()
        self.assertIsNotNone(config.SECRET_KEY)
        self.assertIsNotNone(config.SQLALCHEMY_DATABASE_URL)
        self.assertIsNotNone(config.SMTP_HOST)
        self.assertIsNotNone(config.SMTP_PORT)
        self.assertIsNotNone(config.SMTP_USERNAME)
        self.assertIsNotNone(config.SMTP_PASSWORD)
        self.assertIsNotNone(config.MAIL_FROM)
        self.assertIsNotNone(config.CLOUDINARY_CLOUD_NAME)
        self.assertIsNotNone(config.CLOUDINARY_API_KEY)
        self.assertIsNotNone(config.CLOUDINARY_API_SECRET)
        self.assertIsNotNone(config.REDIS_HOST)
        self.assertIsNotNone(config.REDIS_PORT)
        self.assertIsNotNone(config.ALGORITHM)

if __name__ == '__main__':
    unittest.main()
