// @ts-nocheck
const API_BASE = 'http://127.0.0.1:8000';

export const api = {
    // ดึงข้อมูลพรรคทั้งหมด
    getParties: async () => {
        const res = await fetch(`${API_BASE}/parties/`);
        return res.json();
    },
    // ดึงข้อมูลเขตทั้งหมด
    getConstituencies: async () => {
        const res = await fetch(`${API_BASE}/constituencies/`);
        return res.json();
    },
    // ดึงข้อมูลผู้สมัคร (ที่ Join มาแล้ว)
    getCandidates: async () => {
        const res = await fetch(`${API_BASE}/candidates/`);
        return res.json();
    },

    // ดึงรายชื่อผู้มีสิทธิเลือกตั้ง
    getVoters: async (citizen_id = '') => {
        const url = citizen_id ? `${API_BASE}/voters/?citizen_id=${citizen_id}` : `${API_BASE}/voters/`;
        const res = await fetch(url);
        return res.json();
    },

    // ดึงสถิติผลคะแนน
    getStats: async (const_id = null) => {
        const url = const_id ? `${API_BASE}/results/stats?const_id=${const_id}` : `${API_BASE}/results/stats`;
        const res = await fetch(url);
        return res.json();
    },

    // ดึงจำนวนผู้มาใช้สิทธิ
    getTurnout: async () => {
        const res = await fetch(`${API_BASE}/results/turnout`);
        return res.json();
    },


    // ส่งข้อมูลผู้สมัครใหม่
    createCandidate: async (payload) => {
        const res = await fetch(`${API_BASE}/candidates/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        return res; // ส่ง response กลับไปให้ Action จัดการ error ต่อ
    },
    createParty: async (payload) => {
        return await fetch(`${API_BASE}/parties/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
    },

    createVoter: async (payload) => {
        return await fetch(`${API_BASE}/voters/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
    },

    // เพิ่มเติมใน api object
    getVoterByCitizenId: async (citizen_id) => {
    const res = await fetch(`${API_BASE}/voters/?citizen_id=${citizen_id}`);
    const data = await res.json();
    return data.length > 0 ? data[0] : null; // คืนค่าข้อมูลผู้โหวตคนแรกที่เจอ
}

};