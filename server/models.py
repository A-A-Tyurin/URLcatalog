import csv
import os
import re
from urllib.parse import urlparse
import uuid

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa

from server.utils import query_string_to_dict

db = SQLAlchemy()

class URL(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    uuid = sa.Column(sa.String(36), unique=True, nullable=False)
    scheme = sa.Column(sa.String(10), nullable=False)
    domain = sa.Column(sa.String, nullable=False)
    zone = sa.Column(sa.String(10), nullable=False)
    path = sa.Column(sa.String)
    params = sa.Column(sa.JSON)

    def __repr__(self):
        return f'<URL: id={self.id}, domain={self.domain}>'

    def save(self):    
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'scheme': self.scheme,
            'domain': self.domain,
            'zone': self.zone,
            'path': self.path,
            'params': self.params,
        }

    @classmethod
    def from_string(cls, url):
        parsed_url = urlparse(url)

        if not parsed_url.scheme or not parsed_url.hostname:
            raise ValueError('Wrong URL')

        if not re.match('.*(?=\.)', parsed_url.hostname):
            raise ValueError('Wrong URL')
        
        domain = re.match('.*(?=\.)', parsed_url.hostname).group(0)
        params = query_string_to_dict(parsed_url.query) if parsed_url.query else None
        return cls(
            uuid=str(uuid.uuid1()),
            scheme=parsed_url.scheme,
            domain=domain,
            zone=parsed_url.hostname.replace(domain, ''),
            path=parsed_url.path or None,
            params=params,
        )

    @staticmethod
    def get_objects_from_csv(file_path, remove_file=True):
        total_count, urls = 0, []
       
        with open(file_path, 'r', encoding='utf-8') as file:
            for row in csv.reader(file):
                total_count += 1
                try:
                    urls.append(URL.from_string(*row))
                except ValueError:
                    pass
        
        if remove_file:
            os.remove(file_path)

        return total_count, urls
    
    @staticmethod
    def save_from_objects_list(urls):
        db.session.bulk_save_objects(urls)
        db.session.commit()

