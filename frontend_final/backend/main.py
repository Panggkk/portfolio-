# ==============================================================================
# หน้าที่: ระบบเลือกตั้ง (Backend API)
# ==============================================================================
from typing import List, Dict, Any
from sqlmodel import Session, select, func
from fastapi import FastAPI, HTTPException, Body

from database import engine, init_db
from models import * 

init_db()
app = FastAPI()

# ==========================================
# 1. REGION & CONSTITUENCY API
# ==========================================

@app.post("/regions/")
async def region_create(region: Regions):

    with Session(engine) as session:

        # 1.ตรวจว่า region_id ซ้ำ?
        existing_region = session.get(Regions, region.region_id)
        if existing_region:
            raise HTTPException(
                status_code=400,
                detail="region_id นี้มีอยู่ในระบบแล้ว"
            )

        # 2.ตรวจสอบชื่อภูมิภาค(ตามจังหวัดที่เลือกตั้ง)ซ้ำ?
        duplicate_name = session.exec(
            select(Regions).where(
                Regions.name_th == region.name_th
            )
        ).first()

        if duplicate_name:
            raise HTTPException(
                status_code=400,
                detail=f"ชื่อภูมิภาค '{region.name_th}' มีอยู่ในระบบแล้ว"
            )

        # 3.ตรวจสอบชื่อห้ามว่าง
        if not region.name_th.strip():
            raise HTTPException(
                status_code=400,
                detail="name_th ห้ามเป็นค่าว่าง"
            )

        # 4.ตรวจสอบจำนวนประชากรต้อง >= 0
        if region.total_population < 0:
            raise HTTPException(
                status_code=400,
                detail="total_population ต้องไม่ติดลบ"
            )

        # 5.ผ่านทุกเงื่อนไข บันทึก
        session.add(region)
        session.commit()
        session.refresh(region)

        return region
    
@app.get("/regions/")
async def region_get(region_id: int | None = None):
    """
    ดูรายชื่อภูมิภาค/จังหวัดทั้งหมด
    - ถ้าไม่ระบุ region_id: แสดงทั้งหมด
    - ถ้าระบุ region_id: แสดงเฉพาะจังหวัดนั้น
    """
    with Session(engine) as session:
        # 1. สร้าง Query พื้นฐานดึงจากตาราง Regions
        statement = select(Regions)
        
        # 2. ถ้ามีการระบุ ID มา ให้กรองด้วย WHERE
        if region_id:
            statement = statement.where(Regions.region_id == region_id)
            
        # 3. ประมวลผลดึงข้อมูล
        results = session.exec(statement).all()
        
        # 4. เช็คว่ามีข้อมูลไหม (กรณีระบุ ID แล้วไม่เจอ)
        if region_id and not results:
            raise HTTPException(
                status_code=404, 
                detail=f"ไม่พบข้อมูลภูมิภาคที่มี id: {region_id}"
            )
            
        return results
        

@app.post("/constituencies/")
async def constituency_create(const: Constituencies):

    with Session(engine) as session:

        # 1.ตรวจสอบว่า region มีอยู่จริง
        region = session.get(Regions, const.region_id)
        if region is None:
            raise HTTPException(
                status_code=404,
                detail="ไม่พบ region_id นี้ในระบบ"
            )

        # 2.ตรวจสอบว่า const_id ซ้ำหรือไม่
        existing_const = session.get(Constituencies, const.const_id)
        if existing_const is not None:
            raise HTTPException(
                status_code=400,
                detail="const_id นี้มีอยู่ในระบบแล้ว"
            )

        # 3.ตรวจสอบว่าใน region เดียวกัน มี const_number นี้ไปแล้วหรือยัง
        duplicate_number = session.exec(
            select(Constituencies).where(
                Constituencies.region_id == const.region_id,
                Constituencies.const_number == const.const_number
            )
        ).first()

        if duplicate_number:
            raise HTTPException(
                status_code=400,
                detail=f"region {const.region_id} มีเขตหมายเลข {const.const_number} แล้ว"
            )

        # 4.ตรวจสอบ total_eligible_voters ต้องมากกว่า 0
        if const.total_eligible_voters <= 0:
            raise HTTPException(
                status_code=400,
                detail="จำนวนผู้มีสิทธิเลือกตั้งต้องมากกว่า 0"
            )

        # 5.ผ่านทุกเงื่อนไข ค่อยบันทึก
        session.add(const)
        session.commit()
        session.refresh(const)

        return const

@app.get("/constituencies/")
async def constituency_get(const_id: int | None = None):
    """
    แสดงรายชื่อเขตเลือกตั้งพร้อมรายละเอียดจังหวัด (ข้อ 1)
    - ถ้าไม่ระบุ const_id: แสดงทั้งหมด
    - ถ้าระบุ const_id: แสดงเฉพาะเขตนั้น
    """
    with Session(engine) as session:
        # 1. ใช้ select และ join เพื่อดึงข้อมูลเขตพร้อมชื่อจังหวัด
        statement = (
            select(Constituencies, Regions.name_th)
            .join(Regions, Constituencies.region_id == Regions.region_id)
        )
        
        # 2. กรองข้อมูลกรณีระบุ ID
        if const_id:
            statement = statement.where(Constituencies.const_id == const_id)
            
        results = session.exec(statement).all()
        
        # 3. ตรวจสอบกรณีไม่พบข้อมูล
        if const_id and not results:
            raise HTTPException(
                status_code=404, 
                detail=f"ไม่พบข้อมูลเขตเลือกตั้งที่มี id: {const_id}"
            )
            
        # 4. จัด Format ข้อมูลเพื่อแสดงรายละเอียดตามโจทย์ (2 คะแนน)
        return [
            {
                "const_id": c.const_id,
                "region_name": r_name,
                "const_number": c.const_number,
                "total_eligible_voters": c.total_eligible_voters
            } for c, r_name in results
        ]


# ==========================================
# 2. PARTY & CANDIDATE API 
# ==========================================

@app.post("/parties/")
async def party_create(party: Parties) -> Parties:
    """เพิ่มพรรคการเมือง"""
    with Session(engine) as session:

                # ✅ เช็คก่อนว่ามี party_id นี้หรือยัง
        existing_party = session.get(Parties, party.party_id)

        if existing_party:
            raise HTTPException(
                status_code=400,
                detail="พรรคการเมืองนี้มีอยู่ในระบบแล้ว")
        
        session.add(party)
        session.commit()
        session.refresh(party)
        return party
    
@app.get("/parties/")
async def party_get(party_id: int | None = None, party_name: str | None = None):
    """
    ดูรายชื่อพรรคการเมือง
    - ถ้าไม่ระบุอะไรเลย: แสดงทั้งหมด
    - ถ้าระบุ party_id: แสดงเฉพาะพรรคนั้น
    - ถ้าระบุ party_name: ค้นหาพรรคจากชื่อ
    """
    with Session(engine) as session:
        statement = select(Parties)
        
        # 1. กรองด้วย ID (ถ้ามี)
        if party_id:
            statement = statement.where(Parties.party_id == party_id)
        
        # 2. กรองด้วยชื่อพรรค (ถ้ามี)
        if party_name:
            statement = statement.where(Parties.party_name.contains(party_name))
            
        results = session.exec(statement).all()
        
        # 3. แจ้ง Error ถ้าค้นหาเฉพาะเจาะจงแล้วไม่เจอ
        if (party_id or party_name) and not results:
            raise HTTPException(
                status_code=404, 
                detail="ไม่พบข้อมูลพรรคการเมืองที่ระบุ"
            )
            
        return results


# 2. CANDIDATE API 


@app.post("/candidates/")
async def candidate_create(candidate: Candidates):
    with Session(engine) as session:
        # ตรวจสอบว่า "เขต" (const_id) นี้มีอยู่จริงมั้ย
        # เราดึงข้อมูล constituency มาเพื่อเอาเลข const_number ไปโชว์ตอน return
        constituency = session.get(Constituencies, candidate.const_id)
        if not constituency:
            raise HTTPException(
                status_code=404, 
                detail=f"ไม่พบเขตเลือกตั้งที่มี const_id: {candidate.const_id} ในระบบ"
            )

        # 1. ตรวจสอบว่ามีชื่อนี้อยู่ในระบบแล้วหรือยัง
        existing_candidate = session.exec(
            select(Candidates).where(Candidates.full_name == candidate.full_name)
        ).first()

        if existing_candidate:
            raise HTTPException(
                status_code=400, 
                detail=f"รายชื่อผู้สมัคร '{candidate.full_name}' มีอยู่ในระบบแล้ว"
            )

        # 2. ตรวจสอบว่าในเขตนั้นๆ มีเบอร์นี้ไปแล้วหรือยัง
        existing_number = session.exec(
            select(Candidates).where(
                Candidates.const_id == candidate.const_id,
                Candidates.candidate_number == candidate.candidate_number
            )
        ).first()

        if existing_number:
            raise HTTPException(
                status_code=400, 
                detail=f"เขต {candidate.const_id} มีผู้สมัครเบอร์ {candidate.candidate_number} แล้ว"
            )

        # 3. ตรวจสอบว่าพรรค (party_id) มีอยู่จริงไหม
        party = session.get(Parties, candidate.party_id)
        if not party:
            raise HTTPException(
                status_code=404,
                detail=f"ไม่พบพรรคการเมืองที่มี party_id: {candidate.party_id}"
            )

        # บันทึกลงฐานข้อมูล
        session.add(candidate)
        session.commit()
        session.refresh(candidate)

        # คืนค่ากลับไปพร้อมรายละเอียด const_number และ party_name
        return {
            "candidate_id": candidate.candidate_id,
            "full_name": candidate.full_name,
            "candidate_number": candidate.candidate_number,
            "party_name": party.party_name,
            "const_number": constituency.const_number,
            "status": "บันทึกข้อมูลเรียบร้อย"
        }

@app.get("/candidates/")
async def candidate_get(candidate_id: int | None = None):
    """ดูรายชื่อผู้สมัคร พร้อมรายละเอียดเขตและพรรค (Join 3 ตาราง)"""
    with Session(engine) as session:
        # ใช้ Join เพื่อดึงชื่อพรรคและเลขเขตมาแสดงผล
        statement = (
            select(Candidates, Parties.party_name, Constituencies.const_number)
            .join(Parties, Candidates.party_id == Parties.party_id)
            .join(Constituencies, Candidates.const_id == Constituencies.const_id)
        )
        
        if candidate_id:
            statement = statement.where(Candidates.candidate_id == candidate_id)
            
        results = session.exec(statement).all()
        
        # จัดรูปแบบข้อมูลให้สวยงามและอ่านง่าย
        return [
            {
                "id": c.candidate_id,
                "full_name": c.full_name,
                "candidate_number": c.candidate_number,
                "party": p_name,
                "const_number": c_num
            } for c, p_name, c_num in results
        ]
    

# 3. VOTER API (ข้อ 2)
@app.post("/voters/")
async def voter_create(voter: Voters):
    """เพิ่มผู้มีสิทธิเลือกตั้ง พร้อมเช็คข้อมูลซ้ำและรูปแบบเลขบัตร"""
    with Session(engine) as session:
        
        # 1️⃣ ตรวจสอบว่าเป็นตัวเลขเท่านั้น
        if not voter.citizen_id.isdigit():
            raise HTTPException(
                status_code=400, 
                detail="เลขบัตรประชาชนต้องเป็นตัวเลขเท่านั้น"
            )

        # 2️⃣ ตรวจสอบความยาว 13 หลัก
        if len(voter.citizen_id) != 13:
            raise HTTPException(
                status_code=400, 
                detail="เลขบัตรประชาชนต้องมีความยาว 13 หลัก"
            )

        # 3️⃣ ตรวจสอบว่า "เขต" (const_id) มีอยู่จริง
        constituency = session.get(Constituencies, voter.const_id)
        if not constituency:
            raise HTTPException(
                status_code=404, 
                detail=f"ไม่พบเขตเลือกตั้งที่มี const_id: {voter.const_id}"
            )

        # 4️⃣ ตรวจสอบข้อมูลซ้ำ
        existing_voter = session.exec(
            select(Voters).where(Voters.citizen_id == voter.citizen_id)
        ).first()

        if existing_voter:
            raise HTTPException(
                status_code=400, 
                detail=f"เลขบัตรประชาชน '{voter.citizen_id}' นี้ถูกลงทะเบียนไว้แล้ว"
            )

        # บันทึกข้อมูล
        session.add(voter)
        session.commit()
        session.refresh(voter)

        return {
            "voter_id": voter.voter_id,
            "full_name": voter.full_name,
            "citizen_id": voter.citizen_id,
            "const_number": constituency.const_number,
            "status": "ลงทะเบียนผู้มีสิทธิเลือกตั้งสำเร็จ"
        }

@app.get("/voters/")
async def voter_get(citizen_id: str | None = None):
    """ดูรายชื่อผู้มีสิทธิ พร้อมรายละเอียดเขต (Manual Join)"""
    with Session(engine) as session:
        statement = (
            select(Voters, Constituencies.const_number)
            .join(Constituencies, Voters.const_id == Constituencies.const_id)
        )
        if citizen_id:
            statement = statement.where(Voters.citizen_id == citizen_id)
            
        results = session.exec(statement).all()
        return [
            {
                "full_name": v.full_name,
                "citizen_id": v.citizen_id,
                "const_number": c_num,
                "has_voted_const": v.has_voted_const,
                "has_voted_list": v.has_voted_list
            } for v, c_num in results
        ]

# ==========================================
# 4. VOTING SYSTEM 
# ==========================================

@app.post("/vote/cast")
async def vote_cast(payload: VoteCastRequest):
    with Session(engine) as session:
        # 1.ดึงข้อมูลผู้โหวต
        voter = session.exec(select(Voters).where(Voters.citizen_id == payload.citizen_id)).first()
        if not voter:
            raise HTTPException(status_code=404, detail="ไม่พบรายชื่อผู้มีสิทธิเลือกตั้งในระบบ")

        # 2.ตรวจสอบประเภทการโหวต
        if payload.vote_type == VoteType.constituency:
            # ดึงข้อมูลผู้สมัครมาตรวจสอบเขตก่อน
            candidate = session.get(Candidates, payload.candidate_id)
            if not candidate:
                raise HTTPException(status_code=404, detail="ไม่พบผู้สมัคร")

            # เช็คเขตเลือกตั้ง ว่าตรงกับผู้โหวตไหม
            if candidate.const_id != voter.const_id:
                raise HTTPException(
                    status_code=400, 
                    detail="ไม่สามารถเลือกผู้สมัครต่างเขตได้"
                )

            #ค่อยเช็คว่าเคยใช้สิทธิหรือยัง
            if voter.has_voted_const:
                raise HTTPException(status_code=400, detail="คุณใช้สิทธิเลือก สส.เขต ไปแล้ว")

            voter.has_voted_const = True

        elif payload.vote_type == VoteType.party_list:
            if voter.has_voted_list:
                raise HTTPException(status_code=400, detail="คุณใช้สิทธิเลือกพรรคไปแล้ว")
            
            party = session.get(Parties, payload.party_id)
            if not party:
                raise HTTPException(status_code=404, detail="ไม่พบพรรคการเมือง")
            
            voter.has_voted_list = True

        #  บันทึก Ballot 
        db_ballot = Ballots(
            const_id=voter.const_id,
            candidate_id=payload.candidate_id,
            party_id=payload.party_id,
            vote_type=payload.vote_type
        )

        session.add(db_ballot)
        session.add(voter)
        session.commit()

        return {"message": "บันทึกคะแนนสำเร็จ (Anonymous Recorded)"}


@app.get("/results/turnout")
async def result_turnout(const_id: int | None = None):
    """
    แสดงจำนวนผู้มาใช้สิทธิ
    - แยกตามเขต
    - แยกประเภท เขต / พรรค
    """

    with Session(engine) as session:

        stmt = (
            select(
                Ballots.const_id,
                Ballots.vote_type,
                func.count(Ballots.ballot_id).label("total_votes")
            )
            .group_by(Ballots.const_id, Ballots.vote_type)
        )

        if const_id is not None:
            stmt = stmt.where(Ballots.const_id == const_id)

        results = session.exec(stmt).all()

        return [
            {
                "const_id": const_id,
                "vote_type": vote_type,
                "total_votes": total
            }
            for const_id, vote_type, total in results
        ]


@app.get("/results/stats")
async def result_get_stats(const_id: int | None = None):
    """
    แสดงผลการเลือกตั้ง (ข้อ 4)
    - แยกตามเขต หรือ ภาพรวม
    """
    with Session(engine) as session:
        # 1. เตรียม Query พื้นฐาน (กรองความสัมพันธ์เบื้องต้น)
        # สส. เขต
        cand_query = select(
            Candidates.candidate_id,
            Candidates.full_name, 
            func.count(Ballots.ballot_id).label("total_votes")
        ).join(Ballots, Candidates.candidate_id == Ballots.candidate_id) \
         .where(Ballots.vote_type == VoteType.constituency)

        # พรรค
        party_query = select(
            Parties.party_id,
            Parties.party_name, 
            func.count(Ballots.ballot_id).label("total_votes")
        ).join(Ballots, Parties.party_id == Ballots.party_id) \
         .where(Ballots.vote_type == VoteType.party_list)

        # 2. กรองตามเขต 
        if const_id is not None:
            cand_query = cand_query.where(Ballots.const_id == const_id)
            party_query = party_query.where(Ballots.const_id == const_id)

        # 3. สั่งจัดกลุ่มและเรียงลำดับ
        cand_stmt = cand_query.group_by(Candidates.candidate_id, Candidates.full_name) \
                              .order_by(func.count(Ballots.ballot_id).desc())
        
        party_stmt = party_query.group_by(Parties.party_id, Parties.party_name) \
                                .order_by(func.count(Ballots.ballot_id).desc())

        # 4. ดึงข้อมูลและ Return เป็น Dictionary
        cand_results = session.exec(cand_stmt).all()
        party_results = session.exec(party_stmt).all()

        return {  
            "constituency_results": [
                {"candidate_id": row[0], "full_name": row[1], "votes": row[2]} 
                for row in cand_results
            ],
            "party_list_results": [
                {"party_id": row[0], "party_name": row[1], "votes": row[2]} 
                for row in party_results
            ]
        }
    