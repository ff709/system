#coding:utf8


#数据分析

#导包
from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id
from pyspark.sql.types import StructType,StructField,IntegerType,StringType,FloatType
from pyspark.sql.functions import count,avg,regexp_extract,max
from pyspark.sql.functions import col,sum,when
from pyspark.sql.functions import desc,asc


if __name__ == '__main__':
    #构建
    spark = SparkSession.builder.appName("sparkSQL").master("local[*]").\
        config("spark.sql.shuffle.partitions",2).\
        config("spark.sql.warehouse.dir","hdfs://node1:8020/user/hive/warehouse").\
        config("hive.metastore.uris","thrift://node1:9083").\
        enableHiveSupport().\
        getOrCreate()

    #
    sc = spark.sparkContext

    #读取数据表
    jobData = spark.read.table('jobData')


    #需求1 城市平均工资前十
    top_city = jobData.groupby("city")\
        .agg(avg("maxSalary").alias("avg_max_salary"))\
        .orderBy(desc("avg_max_salary"))

    result1 = top_city.limit(10)

    #sql
    result1.write.mode("overwrite").\
        format("jdbc").\
        option("url","jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8").\
        option("dbtable","averageCity").\
        option("user","root").\
        option("password","root").\
        option("encoding","utf-8").\
        save()

    result1.write.mode("overwrite").saveAsTable("averageCity","parquet")
    spark.sql("select * from averageCity").show()

    #需求二 工资区间

    jobData_classfiy = jobData.withColumn("salary_category",
                                          when(col("maxSalary").between(0,5000),"0-5k")
                                          . when(col("maxSalary").between(5000,7000),"5k-7k")
                                          . when(col("maxSalary").between(7000,10000),"7k-10k")
                                          . when(col("maxSalary").between(10000,20000),"10-20k")
                                          . when(col("maxSalary")>20000,"20k以上")
                                          . otherwise("未分类"))
    result2 = jobData_classfiy.groupby("salary_category").agg(count('*').alias("count"))

    #sql
    result2.write.mode("overwrite").\
        format("jdbc").\
        option("url","jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8").\
        option("dbtable","salarycategory").\
        option("user","root").\
        option("password","root").\
        option("encoding","utf-8").\
        save()

    result2.write.mode("overwrite").saveAsTable("salarycategory","parquet")
    spark.sql("select * from salarycategory").show()

    #需求3 工资经验分析   1. 按照工作经验（`workExperience`）分组，计算每组的最大薪资和最小薪资的平均值
    result3 = jobData.groupby("workExperience")\
        .agg(avg("maxSalary").alias("avg_max_salary"),
             avg("minSalary").alias("avg_min_salary"))\
        .orderBy("workExperience")

    #sql
    result3.write.mode("overwrite").\
        format("jdbc").\
        option("url","jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8").\
        option("dbtable","expSalary").\
        option("user","root").\
        option("password","root").\
        option("encoding","utf-8").\
        save()

    result3.write.mode("overwrite").saveAsTable("expSalary","parquet")
    spark.sql("select * from expSalary").show()

    #城市分布  按照城市（`city`）分组，统计每个城市的职位数量。
    result4 = jobData.groupby("city").count()

    #sql
    result4.write.mode("overwrite").\
        format("jdbc").\
        option("url","jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8").\
        option("dbtable","addresssum").\
        option("user","root").\
        option("password","root").\
        option("encoding","utf-8").\
        save()

    result4.write.mode("overwrite").saveAsTable("addresssum","parquet")
    spark.sql("select * from addresssum").show()


    #需求5 人口区间
    job_df = jobData.withColumn("people_num",when(col("companyPeople").rlike(r'-'),
                                                  regexp_extract(col("companyPeople"),r'(\d+)-(\d+)',1).cast("int"))
                                .otherwise(col("companyPeople").cast("int")))

    people_classify = job_df.withColumn("people_category",
                                          when(col("people_num").between(0,10),"0-10")
                                          . when(col("people_num").between(10,50),"10-50")
                                          . when(col("people_num").between(50,150),"50-150")
                                          . when(col("people_num").between(150,500),"150-500")
                                        .when(col("people_num").between(500, 1000), "500-1000")
                                          . when(col("people_num")>1000,"1000以上")
                                          . otherwise("未分类"))

    result5 = people_classify.groupby("people_category").agg(count('*').alias("count"))

    #sql
    result5.write.mode("overwrite").\
        format("jdbc").\
        option("url","jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8").\
        option("dbtable","peoplecategory").\
        option("user","root").\
        option("password","root").\
        option("encoding","utf-8").\
        save()

    result5.write.mode("overwrite").saveAsTable("peoplecategory","parquet")
    spark.sql("select * from peoplecategory").show()

    #top10
    top_10_salary = jobData.orderBy(col("maxSalary").desc()).limit(10)

    #sql
    top_10_salary.write.mode("overwrite").\
        format("jdbc").\
        option("url","jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8").\
        option("dbtable","salaryTop").\
        option("user","root").\
        option("password","root").\
        option("encoding","utf-8").\
        save()

    top_10_salary.write.mode("overwrite").saveAsTable("salaryTop","parquet")
    spark.sql("select * from salaryTop").show()

    #需求6 薪资分析 行业薪资   按照职位类型（`type`）对数据进行分组，并统计每个职位类型在不同薪资范围内的记录数
    result6 = jobData.groupBy("type").agg(
        sum(when(col("maxSalary") <= 5000, 1).otherwise(0)).alias("0-5000"),
        sum(when((col("maxSalary") > 5000) & (col("maxSalary") <= 7000), 1).otherwise(0)).alias("5000-7000"),
        sum(when((col("maxSalary") > 7000) & (col("maxSalary") <= 10000), 1).otherwise(0)).alias("7000-10000"),
        sum(when((col("maxSalary") > 10000) & (col("maxSalary") <= 20000), 1).otherwise(0)).alias("10000-20000"),
        sum(when(col("maxSalary") > 20000, 1).otherwise(0)).alias("20000以上")
    )

    #sql
    result6.write.mode("overwrite").\
        format("jdbc").\
        option("url","jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8").\
        option("dbtable","typeSalary").\
        option("user","root").\
        option("password","root").\
        option("encoding","utf-8").\
        save()

    result6.write.mode("overwrite").saveAsTable("typeSalary","parquet")
    spark.sql("select * from typeSalary").show()

    #需求7 行业平均薪资
    result7 = jobData.groupby("type").agg(avg(col("maxSalary")).alias("avg_max_salary"))

    #sql
    result7.write.mode("overwrite").\
        format("jdbc").\
        option("url","jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8").\
        option("dbtable","averageType").\
        option("user","root").\
        option("password","root").\
        option("encoding","utf-8").\
        save()

    result7.write.mode("overwrite").saveAsTable("averageType","parquet")
    spark.sql("select * from averageType").show()

    ##需求 经验平均薪资和个数
    result8 = jobData.groupby("workExperience").agg(
        avg(col("maxSalary")).alias("avg_max_salary"),
        count('*').alias("count")
    )

    #sql
    result8.write.mode("overwrite").\
        format("jdbc").\
        option("url","jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8").\
        option("dbtable","averageExperience").\
        option("user","root").\
        option("password","root").\
        option("encoding","utf-8").\
        save()

    result8.write.mode("overwrite").saveAsTable("averageExperience","parquet")
    spark.sql("select * from averageExperience").show()

    #需求9 学历
    result9 = jobData.groupby("education").agg(
        count('*').alias("count")
    )

    #sql
    result9.write.mode("overwrite").\
        format("jdbc").\
        option("url","jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8").\
        option("dbtable","educationCount").\
        option("user","root").\
        option("password","root").\
        option("encoding","utf-8").\
        save()

    result9.write.mode("overwrite").saveAsTable("educationCount","parquet")
    spark.sql("select * from educationCount").show()

    #行业个数
    result10 = jobData.groupby("type").agg(
        count('*').alias("count")
    )

    #sql
    result10.write.mode("overwrite").\
        format("jdbc").\
        option("url","jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8").\
        option("dbtable","typeCount").\
        option("user","root").\
        option("password","root").\
        option("encoding","utf-8").\
        save()

    result10.write.mode("overwrite").saveAsTable("typeCount","parquet")
    spark.sql("select * from typeCount").show()

    #需求11 各类型薪资最大值
    result11 = jobData.groupby("type").agg(
        max(col("maxSalary")).alias("max_salary")
    )

    #sql
    result11.write.mode("overwrite").\
        format("jdbc").\
        option("url","jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8").\
        option("dbtable","typeMax").\
        option("user","root").\
        option("password","root").\
        option("encoding","utf-8").\
        save()

    result11.write.mode("overwrite").saveAsTable("typeMax","parquet")
    spark.sql("select * from typeMax").show()

    #各城市薪资情况
    conditions = [
        (col("maxSalary") <= 5000, '0-5000'),
        ((col("maxSalary") > 5000) & (col("maxSalary") <= 7000), '5000-7000'),
        ((col("maxSalary") > 7000) & (col("maxSalary") <= 10000), '7000-10000'),
        ((col("maxSalary") > 10000) & (col("maxSalary") <= 20000), '10000-20000'),
        (col("maxSalary") > 20000, '20000以上')
    ]

    result12 = jobData.groupby("city").agg(
        *[count(when(condition,1)).alias(range_name) for condition,range_name in conditions]
    )
    #sql
    result12.write.mode("overwrite").\
        format("jdbc").\
        option("url","jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8").\
        option("dbtable","citySalary").\
        option("user","root").\
        option("password","root").\
        option("encoding","utf-8").\
        save()

    result12.write.mode("overwrite").saveAsTable("citySalary","parquet")
    spark.sql("select * from citySalary").show()


    #城市人数
    conditionsTwo = [
        (col("people_num") <= 10, '0-10'),
        ((col("people_num") > 10) & (col("people_num") <= 50), '10-50'),
        ((col("people_num") > 50) & (col("people_num") <= 150), '50-150'),
        ((col("people_num") > 150) & (col("people_num") <= 500), '150-500'),
        ((col("people_num") > 500) & (col("people_num") <= 1000), '500-1000'),
        (col("people_num") > 1000, '1000以上')
    ]

    result13 = job_df.groupby("city").agg(
        *[count(when(condition,1)).alias(range_name) for condition,range_name in conditionsTwo]
    )
    #sql
    result13.write.mode("overwrite").\
        format("jdbc").\
        option("url","jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8").\
        option("dbtable","cityPeople").\
        option("user","root").\
        option("password","root").\
        option("encoding","utf-8").\
        save()

    result13.write.mode("overwrite").saveAsTable("cityPeople","parquet")
    spark.sql("select * from cityPeople").show()




