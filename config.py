import os
SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enables debug mode.
DEBUG = True

tokens = {
    "assistant_auth": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklxTVg0OXlRejNLZWwyX2RsY3RtWSJ9.eyJpc3MiOiJodHRwczovL2FuaC03LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MjE5MmU5OGVhZTkxZjAwNmEwYWNhOGUiLCJhdWQiOiJBZ2VuY3kiLCJpYXQiOjE2NDkxMjYwMzYsImV4cCI6MTY0OTIxMjQzNiwiYXpwIjoiUnhDamNrYkswbmNoUkVrSkxOUm5KZFA1c3p0dlB0ZUwiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvciIsImdldDptb3ZpZSJdfQ.g0ZQuUJnnfirx9DFGKF-gYPVH7REmPBKqfwPdqxxdJkRspIhMu-IAiOjopGnH3aLOSa-m-QIVrr_vstCC0mN_QMWZtO2-T1Gx6nLeKZJVPaQzmTlGYqjPyzwuZIIcRXP3dH8efPrOiu-nx4NXA9saaZeKuLMTj_t2ytyZDBeGpreXqx_-TDHo5q68p4n01gN1kkdMLe3RSKWN9aeOHRAanwcM1qdOfxsYgUO10kfkd9L9D6IQYEiqUF767ZaPUygVH-TtEjH9NIfAW1qAoH7cgCYNXSP96fCm88i9u6QMWhCMFcQnrZCpZGA0hN9LCpt4Xj3kd7INxa_NOQuzYw3Fw",
    "director_auth": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklxTVg0OXlRejNLZWwyX2RsY3RtWSJ9.eyJpc3MiOiJodHRwczovL2FuaC03LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MjE5MmVlYzg2N2M0ZDAwNzU3OTlkYTEiLCJhdWQiOiJBZ2VuY3kiLCJpYXQiOjE2NDkxMjU5MDIsImV4cCI6MTY0OTIxMjMwMiwiYXpwIjoiUnhDamNrYkswbmNoUkVrSkxOUm5KZFA1c3p0dlB0ZUwiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImdldDphY3RvciIsImdldDptb3ZpZSIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIl19.Ln5NtGzkZLltyEtunEPFjmNA4v5yMbgrmxC1cWVc7PX9pnpavhjnp7MlB4M6UCYxab5UE8jmM3lWsFeJz7ppBmqTnOL8egXitudnoIzY8ku7F_LzuiKxA_xuH2_VMjia_ljDf3EjGp4M1z5TZI5mp-E32DSbOvOm_eSNqClQi17FQX2A53ImRUP4fmXWVvOhizmzEygFx6P6a_i4fOSDssMSqS9Q5OFLnplSng13I6p7C-0bYrJs6-U8Jx_YwHvq5BJ_NWeyIMpO2VKC9XYTAbT8YaTlxtMz_OzuBvToo8FoykZodTGzAKb8UcWfoAtmgo5JcBvwcSpNco5jxwqClA",
    "producer_auth": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklxTVg0OXlRejNLZWwyX2RsY3RtWSJ9.eyJpc3MiOiJodHRwczovL2FuaC03LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MjE5MmYzNTE2NzFjOTAwNjgzNDRhYjAiLCJhdWQiOiJBZ2VuY3kiLCJpYXQiOjE2NDkxMjU2NzUsImV4cCI6MTY0OTIxMjA3NSwiYXpwIjoiUnhDamNrYkswbmNoUkVrSkxOUm5KZFA1c3p0dlB0ZUwiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvciIsImdldDptb3ZpZSIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.olhoOZ6D-nKpCbdYveY_LTX_5iRcxzr2Q78qhiCWpE00P67ARIRzgo4W-SMA29acGQTLk4fUCRnZ0EPHgmA1QDO63a169pyEn0AqzV_Zkbr1vcflDFbBIkk75YAFwZZ_dZ3icG8AnHYVovgAqCRbRKgWWEdqRKCcVFANGsrvPWhzq6hdl53qu7qV2qVBEl361DNUib2hx34dVcpZ5q1O5WtJPDFHZkXrO1pAey5VsJcIqv0Uq-0KplpEjlHKImcPlLsVo9BEJ0JdJ0IZVmaOZg7wHxokT12wv9XV-dSkQm3r17K54nwJogy6MC0kFT2WyOz7LU0IajIjJtfgb2bI_g"

}
# Database URL
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost:5432/agency'
SQLALCHEMY_TRACK_MODIFICATIONS = False
