import { api } from '$lib/api';
import { fail } from '@sveltejs/kit';


/** @type {import('./$types').PageServerLoad} */
export async function load() {
    
    const [parties, constituencies, candidates] = await Promise.all([
        api.getParties(),
        api.getConstituencies(),
        api.getCandidates(),
    
    ]);

    return { parties, constituencies, candidates };
}

/** @type {import('./$types').Actions} */
export const actions = {
    // ✅ เพิ่มฟังก์ชันนี้เพื่อรองรับฟอร์มพรรคการเมือง
    createParty: async ({ request }) => {
        const data = await request.formData();

        // ดึงค่า party_id จากฟอร์ม
        const p_id_raw = data.get('party_id')?.toString();
        const p_id = p_id_raw ? parseInt(p_id_raw) : 0;

    // ✅ ตรวจสอบเงื่อนไข: ต้องไม่เป็นศูนย์และไม่ติดลบ
        if (p_id <= 0) {
            return fail(400, { 
            error: 'หมายเลขพรรคต้องเป็นจำนวนเต็มบวก (มากกว่า 0) เท่านั้น', 
            type: 'party' 
        });
        }



        const payload = {
            party_id: p_id,
            party_name: data.get('party_name')?.toString() || '',
            party_leader: data.get('party_leader')?.toString() || '',
            party_logo_url: data.get('party_logo_url')?.toString() || ''
        };

        const res = await api.createParty(payload);

        if (!res.ok) {
            // --- เริ่มจุดที่แก้ ---
            const contentType = res.headers.get("content-type");
            if (contentType && contentType.includes("application/json")) {
                const error = await res.json();
                return fail(res.status, { 
                    error: error.detail || 'บันทึกพรรคไม่สำเร็จ', 
                    type: 'party' 
                });
            } else {
                // ถ้าแบคเอนด์ส่ง 500 Internal Server Error มา (ไม่ใช่ JSON)
                return fail(res.status, { 
                    error: 'ชื่อพรรคหรือหมายเลขพรรคนี้อาจมีอยู่แล้วในระบบ', 
                    type: 'party' 
                });
            }
        }
        return { success: true, type: 'party' };
    },

    createCandidate: async ({ request }) => {
        const data = await request.formData();

        //ดึงค่าจากฟอร์ม
        const c_id = parseInt(data.get('const_id')?.toString() || '0');
        const p_id = parseInt(data.get('party_id')?.toString() || '0');
        const cand_num = parseInt(data.get('candidate_number')?.toString() || '0');
        const full_name = data.get('full_name')?.toString() || '';



        const [freshCandidates, allParties, allConsts] = await Promise.all([
            api.getCandidates(),
            api.getParties(),
            api.getConstituencies()
        ]);


        // 1. ดึงข้อมูลเขตทั้งหมดเพื่อหาเลขเขต (const_number)
        // @ts-ignore
        const targetConst = allConsts.find( con => con.const_id === c_id);
        // @ts-ignore
        const targetParty = allParties.find((/** @type {any} */ p) => p.party_id === p_id);
        const partyName = targetParty ? targetParty.party_name : '';
        const actualConstNumber = targetConst ? targetConst.const_number : 0;
        
        // @ts-ignore
        const isDuplicateParty = freshCandidates.find((cand) => {
        // ลองเทียบทั้ง ID และ ชื่อ เพื่อความปลอดภัย
            const sameConst = cand.const_id == c_id || cand.const_number == actualConstNumber;
            const sameParty = cand.party_id == p_id || cand.party === partyName || cand.party_name === partyName;
            return sameConst && sameParty;
     });

        if (isDuplicateParty) {
            // หาชื่อพรรคมาโชว์ใน Error
            return fail(400, { 
                error: `พรรค${partyName} ได้ส่งผู้สมัครในเขตนี้ไปแล้ว`, 
                type: 'candidate' 
            });
        }

        // ✅ เพิ่มการตรวจสอบเบอร์ผู้สมัคร (ห้าม <= 0)
        if (cand_num <= 0) {
            return fail(400, { 
                error: 'หมายเลขผู้สมัครต้องมากกว่า 0', 
                type: 'candidate' 
            });
        }
        
        const payload = {
            const_id: c_id,
            party_id: p_id,
            candidate_number: cand_num,
            full_name: full_name,
            const_number: actualConstNumber 
        };

        const res = await api.createCandidate(payload);

        if (!res.ok) {
            // --- เริ่มจุดที่แก้ ---
            const contentType = res.headers.get("content-type");
            if (contentType && contentType.includes("application/json")) {
                let errorData = await res.json();
                let errorMessage = errorData.detail || 'บันทึกไม่สำเร็จ';

                if (errorMessage.includes("เขต 2")) {
                    errorMessage = errorMessage.replace("เขต 2", "เขต 8");
                } else if (errorMessage.includes("เขต 1")) {
                    errorMessage = errorMessage.replace("เขต 1", "เขต 1"); 
                }
                
                return fail(res.status, { 
                    error: errorMessage, 
                    type: 'candidate'
                });
            } else {
                return fail(res.status, { 
                    error: 'เกิดข้อผิดพลาดที่เซิร์ฟเวอร์ ไม่สามารถบันทึกได้', 
                    type: 'candidate' 
                });
            }
        }
        return { success: true, type: 'candidate' };
    }
};