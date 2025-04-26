from pydantic import BaseModel
from typing import List

class Location(BaseModel):
    address: str
    postalCode: str
    city: str
    countryCode: str
    region: str

class Profile(BaseModel):
    network: str
    username: str
    url: str

class Basics(BaseModel):
    name: str
    label: str
    image: str
    email: str
    phone: str
    url: str
    summary: str
    location: Location
    profiles: List[Profile]

class Work(BaseModel):
    name: str
    location: str
    description: str
    position: str
    url: str
    startDate: str
    endDate: str
    summary: str
    highlights: List[str]

class Education(BaseModel):
    institution: str
    url: str
    area: str
    studyType: str
    startDate: str
    endDate: str
    score: str
    courses: List[str]

class Skill(BaseModel):
    name: str
    level: str
    keywords: List[str]

class Project(BaseModel):
    name: str
    description: str
    highlights: List[str]
    keywords: List[str]
    startDate: str
    endDate: str
    url: str
    roles: List[str]
    entity: str
    type: str

class Resume(BaseModel):
    basics: Basics
    work: List[Work]
    education: List[Education]
    skills: List[Skill]
    projects: List[Project]
