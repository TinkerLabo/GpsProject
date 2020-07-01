FROM python:3
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get install -y vim less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

RUN pip install numpy pandas matplotlib networkx pyyaml xlsxwriter tornado pillow colour colour-science requests
RUN apt-get update
RUN apt-get install -y apt-utils apt-transport-https  figlet cron
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/8/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN sed -i -e "s/MinProtocol = TLSv1.2/MinProtocol = TLSv1.0/" /etc/ssl/openssl.cnf
RUN sed -i -e "s/CipherString = DEFAULT@SECLEVEL=2/CipherString = DEFAULT@SECLEVEL=1/" /etc/ssl/openssl.cnf
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools unixodbc-dev   
RUN pip install --upgrade pip
RUN pip install pyodbc
#RUN wget https://gallery.technet.microsoft.com/ODBC-Driver-13-for-Ubuntu-b87369f0/file/154097/2/installodbc.sh
#RUN bash installodbc.sh
RUN pip install --upgrade pip
RUN pip install beautifulsoup4
RUN pip install requests

RUN pip install selenium
RUN apt-get install -y wget libfontconfig
#RUN mkdir -p /home/root/src && cd $_ && wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
#RUN cd /home/root/src && tar jxvf phantomjs-2.1.1-linux-x86_64.tar.bz2
#RUN cd /home/root/src/phantomjs-2.1.1-linux-x86_64/bin && cp phantomjs /usr/local/bin/
# ユーザ作成
RUN groupadd web
RUN useradd -d /home/python -m python
