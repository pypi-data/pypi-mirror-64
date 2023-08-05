####################################################################
#                                                                  #
# Wilfred                                                          #
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>, et al. #
#                                                                  #
# Licensed under the terms of the MIT license, see LICENSE.        #
# https://github.com/wilfred-dev/wilfred                           #
#                                                                  #
####################################################################

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from appdirs import user_data_dir
from os.path import isdir
from pathlib import Path


if not isdir(f"{user_data_dir()}/wilfred"):
    Path(f"{user_data_dir()}/wilfred").mkdir(parents=True, exist_ok=True)

database_path = f"{user_data_dir()}/wilfred/wilfred.sqlite"
engine = create_engine(f"sqlite:///{database_path}")
Base = declarative_base()


class Server(Base):
    __tablename__ = "servers"

    id = Column(String, primary_key=True, unique=True)
    name = Column(String, unique=True)
    image_uid = Column(String)
    memory = Column(Integer)
    port = Column(Integer, unique=True)
    custom_startup = Column(String)
    status = Column(String)

    environment_variables = relationship("EnvironmentVariable")

    def __repr__(self):
        return f"<Server(id='{self.id}', name='{self.name}', image_uid='{self.image_uid}', port='{self.port}')>"


class EnvironmentVariable(Base):
    __tablename__ = "environment_variables"

    id = Column(Integer, primary_key=True)
    server_id = Column(String, ForeignKey("servers.id"), unique=False)
    variable = Column(String)
    value = Column(String)


Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
