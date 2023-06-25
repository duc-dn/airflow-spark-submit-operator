from pyspark.sql import SparkSession

MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
MINIO_SERVER_HOST = "http://minio:9000"


spark = (
    SparkSession.builder.config(
        "spark.jars.packages",
        "org.apache.spark:spark-avro_2.12:3.2.0,"
        "org.apache.hadoop:hadoop-aws:3.2.0,"
        "com.amazonaws:aws-java-sdk:1.11.375,"
        "org.apache.spark:spark-tags_2.12:3.2.0,"
        "org.apache.hadoop:hadoop-common:3.2.0",
    )
    .config(
        "spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem"
    )
    .config("spark.hadoop.fs.s3a.access.key", MINIO_ACCESS_KEY)
    .config("spark.hadoop.fs.s3a.secret.key", MINIO_SECRET_KEY)
    .config("spark.hadoop.fs.s3a.endpoint", MINIO_SERVER_HOST)
    .config("spark.hadoop.fs.s3a.path.style.access", "true")
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
    .config(
        "spark.hadoop.fs.s3a.aws.credentials.provider",
        "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
    )
    .getOrCreate()
)

columns = ["Seqno","Quote"]
data = [("1", "Be the change that you wish to see in the world"),
    ("2", "Everyone thinks of changing the world, but no one thinks of changing himself."),
    ("3", "The purpose of our lives is to be happy."),
    ("4", "Be cool.")]

df = spark.createDataFrame(data,columns)
df.show(truncate=False)

df.write.format("csv").mode("append").save("s3a://datalake/test")
