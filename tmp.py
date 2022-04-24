def slowly_changing_dimension_type1(df: DataFrame, key_column: str, date_column: str):
"""
Build a dataframe containing only the most recent records for each key
:param df: Dataframe to transform
:param primary_key_column: A Key Column on which to filter records
:param date_column: a date column to filter most recent keys
:return: Dataframe containing only the most recent records for each key
"""
most_recent_df = (
df.groupBy(key_column)
.agg(F.max(F.col(date_column)).alias("max_date"))
.select(key_column, "max_date")
) df = (
df.join(most_recent_df, how="inner", on=[key_column])
.where(F.col(date_column) == most_recent_df.max_date)
.drop("max_date")
)
df = df.dropDuplicates([key_column])
return df


def hash_columns(df: DataFrame, column_name: str, columns: List[str], algorithm="SHA1"):
"""
Create a new column with unique key
:param df: DataFrame
:param columns: List of columns to include in the key
:param column_name: Output column name
:param algorithm: Hashing Algorithm (MD5, SHA1, SHA256
:return: a DataFrame with a unique_key column
"""
if algorithm == "MD5":
return df.withColumn(column_name, F.upper(F.md5(F.concat_ws("_", *columns))))
elif algorithm == "SHA1":
return df.withColumn(column_name, F.upper(F.sha1(F.concat_ws("_", *columns))))
elif algorithm == "SHA256":
return df.withColumn(
column_name, F.upper(F.sha2(F.concat_ws("_", *columns), 256))
)
else:
return df