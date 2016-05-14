FROM python:2.7.11-onbuild

RUN rm koyrelengde_per_person.png
CMD python ./koyrelengde.py --docker

