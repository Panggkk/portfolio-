// @ts-nocheck
import { api } from '$lib/api';
import { fail } from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load() {
    const [candidates, parties, constituencies, voters, turnout] = await Promise.all([
        api.getCandidates(),
        api.getParties(),
        api.getConstituencies(),
        api.getVoters(),
        api.getTurnout()
    ]);

    // ✅ สร้างรายงานสรุปยอดผู้มาใช้สิทธิรายเขต (อ้างอิงจากข้อมูลล่าสุด)
    const turnout_report = constituencies.map(con => {
        const c_vote = turnout.find(t => t.const_id === con.const_id && t.vote_type === 'Constituency');
        const p_vote = turnout.find(t => t.const_id === con.const_id && t.vote_type === 'PartyList');
        return {
            region_name: con.region_name,
            const_number: con.const_number,
            const_count: c_vote ? c_vote.total_votes : 0,
            party_count: p_vote ? p_vote.total_votes : 0
        };
    });

    return { candidates, parties, constituencies, voters, turnout_report };
}

/** @type {import('./$types').Actions} */
export const actions = {
    castVote: async ({ request }) => {
        const data = await request.formData();
        const citizen_id = data.get('citizen_id')?.toString();
        const candidate_id = data.get('candidate_id');
        const party_id = data.get('party_id'); 
        const vote_type = data.get('vote_type')?.toString();

        

        // 1. ดึงข้อมูลผู้โหวตเพื่อเช็กเขตและสิทธิ
        const voterList = await api.getVoters(citizen_id);
        const voter = voterList && voterList.length > 0 ? voterList[0] : null;
        if (!voter) return fail(400, { error: 'ไม่พบข้อมูลผู้มีสิทธิ์ในระบบ' });

        // 2. เช็กการลงคะแนนซ้ำ
        if (vote_type === 'Constituency' && voter.has_voted_const) {
            return fail(400, { error: 'ท่านได้ใช้สิทธิเลือก ส.ส.เขต ไปแล้ว' });
        }
        if (vote_type === 'PartyList' && voter.has_voted_list) {
            return fail(400, { error: 'ท่านได้ใช้สิทธิเลือกพรรคการเมืองไปแล้ว' });
        }

        // 3. ถ้าเป็น ส.ส.เขต เช็กว่าเลือกผู้สมัครตรงเขตตัวเองไหม (ยกเว้นกรณี No Vote)
        if (vote_type === 'Constituency' ) {
            const allCandidates = await api.getCandidates();
            const targetCandidate = allCandidates.find(c => String(c.id) === String(candidate_id));
            
            if (!targetCandidate) {
                return fail(400, { error: 'เลือกผู้สมัคร' });
            }

            if (targetCandidate.const_id !== voter.const_id) {
                return fail(400, { error: 'คุณไม่มีสิทธิ์เลือกผู้สมัครนอกเขตเลือกตั้งของตนเอง' });
            }
        }

        // 4. ส่งข้อมูลไปบันทึกที่ Backend
        const payload = {
            citizen_id,
            vote_type,
            candidate_id: candidate_id ? parseInt(candidate_id) : null,
            party_id: party_id ? parseInt(party_id) : null
        };

        try {
            const res = await fetch('http://127.0.0.1:8000/vote/cast', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!res.ok) {
                const errorData = await res.json();
                return fail(res.status, { error: errorData.detail || 'การลงคะแนนไม่สำเร็จ' });
            }

            return { success: true, message: 'บันทึกคะแนนสำเร็จ' };

        } catch (e) {
            return fail(500, { error: 'ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์ฐานข้อมูลได้' });
        }
    }
};