def getFilePath(bucket,prefix):
    """ List all files (sorted) in the specified bucket
    
    Arguments:
        - bucket [str] -- S3 bucket to search
        - prefix [str] -- S3 prefix
    
    Returns:
        - List of files in bucket
    """
    s3resource = boto3.resource("s3")
    s3bucket = s3resource.Bucket(bucket)
    pathsToCsv = []
    
    for objectSummary in list(s3bucket.objects.filter(Prefix=prefix))[0:]:
        pathsToCsv.append(objectSummary.key)
    pathsToCsv = [file.replace(prefix,"") for file in pathsToCsv if file != prefix]
    pathsToCsv = [file for file in pathsToCsv if not "/" in file]
    return(sorted(pathsToCsv))

def importFileFromS3(bucket, key,fileFormat="csv",sep=",",header="infer",parse_dates=False,encoding="utf-8",decimal="."):
    """ Load meta data from S3 to Pandas

    Arguments:
        - bucket [str]       -- S3 bucket where file is located
        - key [str]          -- S3 key to find file (no leading "/")
        - fileFormat = [str] -- File format used for import ("csv"/"xlsx"/"pkl", default == "csv")
        
    Returns:
        - df [pd.DataFrame] 
    """
    s3client = boto3.client("s3")
    s3resource = boto3.resource("s3")   
    obj = s3client.get_object(Bucket=bucket,Key=key)
    data = obj["Body"].read()
    
    if fileFormat == "csv":
        df = pd.read_csv(io.BytesIO(data),sep=sep,header=header,parse_dates=parse_dates,encoding=encoding,decimal=decimal)
    elif fileFormat == "xlsx":
        df = pd.read_excel(io.BytesIO(data), encoding="utf-8")
    elif fileFormat == "pkl":
        df = pd.read_pickle(io.BytesIO(data))
    else:
        raise("File format ({}) not supported".format(fileFormat))
    return df

def exportPandasToS3(df,bucket,key,fileFormat="csv"):
    """ Export Pandas df as csv to specified bucket/key

    Arguments:
        - df [pd.DataFrame]  -- DataFrame to export 
        - bucket [str]       -- S3 bucket where file is located
        - key [str]          -- S3 key to find file (no leading "/")
        - fileFormat = [str] -- File format used for export (default == "csv")
    """
    
    s3client = boto3.client("s3")
    s3resource = boto3.resource("s3")   
    
    if fileFormat == "csv":
        buffer = io.StringIO()
        df.to_csv(buffer,index=False)    
        s3resource.Object(bucket, key).put(Body=buffer.getvalue())
    elif fileFormat == "xlsx":
        
        with io.BytesIO() as output:
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df.to_excel(writer)
            data = output.getvalue()
            s3resource.Object(bucket, key).put(Body=data)
            
    elif fileFormat == "pkl":
        serializedMyData = pickle.dumps(df)
        s3resource.Object(bucket, key).put(Body=serializedMyData)
    else:
        raise("File format ({}) not supported".format(fileFormat))