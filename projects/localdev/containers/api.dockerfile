FROM python:3.9

COPY projects/shared/api_requirements.txt  /opt/api/requirements.txt
RUN pip3 install pip==21.3.1 setuptools==59.1.1 \
    && pip3 install --no-deps -r /opt/api/requirements.txt \
    && pip3 check

COPY src/vc_api/ /opt/vc_api/

RUN pip3 install --no-deps \
    /opt/vc_api \
    && pip3 check

COPY projects/shared/api_entrypoint.sh /opt/api/
RUN chmod +x /opt/api/api_entrypoint.sh

WORKDIR /opt/api