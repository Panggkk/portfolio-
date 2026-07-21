import { api } from '$lib/api'; // สมมติว่าไฟล์ api.js อยู่ใน src/lib
import { fail } from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load() {
    // ดึงข้อมูลผู้มีสิทธิเลือกตั้งและรายชื่อเขตมาพร้อมกัน
    const [rawVoters, constituencies] = await Promise.all([
        api.getVoters(),
        api.getConstituencies()
    ]);


    // แปลงข้อมูลผู้มีสิทธิเลือกตั้งให้อยู่ในรูปแบบที่ต้องการ (ถ้าจำเป็น)
    // @ts-ignore
    const voters = rawVoters.map((voter) => {
    const targetConst = constituencies.find(
        // @ts-ignore
        (c) => Number(c.const_number) === Number(voter.const_number)
    );

    return {
        ...voter,
        region_name: targetConst?.region_name || 'ไม่ระบุจังหวัด',
        const_number: targetConst?.const_number || '-'
    };
});
    return {
        voters,
        constituencies
    };
}

/** @type {import('./$types').Actions} */
export const actions = {
    // Action สำหรับเพิ่มรายชื่อผู้มีสิทธิ
    addVoter: async ({ request }) => {
        const data = await request.formData();
        const citizen_id = data.get('citizen_id')?.toString() || '';
        const full_name = data.get('full_name')?.toString() || '';

        const const_id_raw = data.get('const_id'); // เก็บค่า raw ไว้ก่อนแปลง

        if(!citizen_id || !full_name || !const_id_raw) {
            return fail(400, { message: 'กรุณากรอกข้อมูลให้ครบถ้วน', error: true });
        }

        const payload = {
            citizen_id,
            full_name,
            const_id: parseInt(const_id_raw.toString())
        };

        const res = await api.createVoter(payload);

        if (!res.ok) {
            const error = await res.json();
            return fail(400, { message: error.detail, error: true });
        }

        return { success: true };
    },

   
};