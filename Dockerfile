FROM python:3
ADD config.py /
ADD stan.py /
RUN pip install requests
CMD ["python", "./stan.py"]