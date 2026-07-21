from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator, model_validator
from sqlmodel import Field, SQLModel, DateTime,  Column, func
from enum import Enum


class VoteType(str, Enum):
    constituency = "Constituency"
    party_list = "PartyList"

# ตารางภูมิภาค (Regions)
class Regions(SQLModel, table=True):
    region_id: int = Field(default=None, primary_key=True)
    name_th: str = Field(nullable=False)
    total_population: int = Field(default=0)

#ตารางเขตเลือกตั้ง (Constituencies)
class Constituencies(SQLModel, table=True):
    const_id: int = Field(default=None, primary_key=True)
    region_id: int = Field(nullable=False)
    const_number: int = Field(nullable=False)
    total_eligible_voters: int = Field(default=0)

#ตารางพรรคการเมือง (Parties)
class Parties(SQLModel, table=True):
    party_id: Optional[int] = Field(default=None, primary_key=True)
    party_name: str = Field(unique=True, nullable=False)
    party_leader: Optional[str] = None
    party_logo_url: Optional[str] = None

# ตารางผู้สมัคร สส. เขต (Candidates)
class Candidates(SQLModel, table=True):
    candidate_id: Optional[int] = Field(default=None, primary_key=True)
    const_id: int = Field(nullable=False)
    const_number: int = Field(nullable=False)
    party_id: int = Field(nullable=False)
    candidate_number: int = Field(nullable=False)
    full_name: str = Field(nullable=False)

# 5. ตารางผู้มีสิทธิเลือกตั้ง (Voters)
class Voters(SQLModel, table=True):
    voter_id: Optional[int] = Field(default=None, primary_key=True)
    citizen_id: str = Field(unique=True, nullable=False)
    full_name: str = Field(nullable=False)
    const_id: int = Field(nullable=False)  ##id เขตเลือกตั้ง
    has_voted_const: bool = Field(default=False)
    has_voted_list: bool = Field(default=False)

# 6. ตารางบันทึกคะแนน (Ballots)
class Ballots(SQLModel, table=True):
    ballot_id: Optional[int] = Field(default=None, primary_key=True)
    const_id: int = Field(nullable=False)
    candidate_id: Optional[int] = Field(default=None)
    party_id: Optional[int] = Field(default=None)
    vote_type: VoteType = Field(nullable=False) # 'Constituency' หรือ 'PartyList'
    
    voted_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

    @model_validator(mode="after")
    def check_vote_target(self):
        if self.vote_type == VoteType.constituency:
            if self.candidate_id is None:
                raise ValueError("Constituency vote ต้องมี candidate_id")
            if self.party_id is not None:
                raise ValueError("Constituency vote ห้ามมี party_id")

        if self.vote_type == VoteType.party_list:
            if self.party_id is None:
                raise ValueError("PartyList vote ต้องมี party_id")
            if self.candidate_id is not None:
                raise ValueError("PartyList vote ห้ามมี candidate_id")

        return self


class VoteCastRequest(BaseModel):
    citizen_id: str = Field(..., min_length=13, max_length=13)
    vote_type: VoteType
    candidate_id: Optional[int] = None
    party_id: Optional[int] = None

    @field_validator("citizen_id")
    def validate_citizen_id(cls, v):
        if not v.isdigit():
            raise ValueError("เลขบัตรต้องเป็นตัวเลขเท่านั้น")
        return v