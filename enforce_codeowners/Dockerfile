FROM python

RUN pip install PyGithub

COPY ./ ./enforce_codeowners
RUN pip install -e enforce_codeowners
