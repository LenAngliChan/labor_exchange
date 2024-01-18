from fastapi import HTTPException, status

token_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid auth token")
credentials_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")
client_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Can't find this User!")
job_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Can't find this Job!")
access_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You dont own this item!")
companies_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Only companies can create or change jobs!")
applicants_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                     detail="Only applicants can create or change responses!")
