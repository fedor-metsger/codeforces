
import atexit
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, registry

from config.settings import BASE_DIR


load_dotenv(BASE_DIR / '.env')

PG_USER = os.getenv("DB_USER", "postgres")
PG_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
PG_DB = os.getenv("DB_NAME", "postgres")
PG_HOST = os.getenv("DB_HOST", "localhost")
PG_PORT = os.getenv("DB_PORT", 5432)
PG_DSN = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"


engine = create_engine(PG_DSN)
atexit.register(engine.dispose)

Session = sessionmaker(bind=engine)
Base = declarative_base()

mapper_registry = registry()
metadata_obj = MetaData()
metadata_obj.reflect(bind=engine)
tag_table = metadata_obj.tables["problems_tag"]
problem_table = metadata_obj.tables["problems_problem"]
belonging_table = metadata_obj.tables["problems_belonging"]


class Tag:
    pass


mapper_registry.map_imperatively(Tag, tag_table)


class Problem:
    pass


mapper_registry.map_imperatively(Problem, problem_table)


class Belonging:
    pass


mapper_registry.map_imperatively(Belonging, belonging_table)


def get_topics():
    tags = Session().query(Tag)
    result = {}
    for t in tags:
        # result.append({"id": t.id, "name": t.name})
        result[str(t.id)] = t.name
    return result


def get_problems_by_tag(tag: int):
    problems = Session().query(Belonging, Problem).filter(
        Belonging.problem_id == Problem.id).filter(Belonging.tag_id == tag)
    result = []
    for b, p in problems:
        result.append({"number": p.number, "name": p.name, "difficulty": p.difficulty})
    return result
