// @ts-nocheck
import { api } from '$lib/api';

/** @type {import('./$types').PageServerLoad} */
export async function load({ url }) {
    // 1. ดึงค่า const_id จาก Query Parameter (เช่น /results?const_id=1)
    const constIdParam = url.searchParams.get('const_id');
    const const_id = constIdParam ? parseInt(constIdParam) : null;

    // 2. ดึงข้อมูลที่จำเป็นมาพร้อมกัน
    const [stats, constituencies,candidates] = await Promise.all([
        api.getStats(const_id),
        api.getConstituencies(),
        api.getCandidates()
    ]);

    const enrichedConstituencyResults = stats.constituency_results.map((/** @type {any} */ cand) => {
        // ค้นหาข้อมูลผู้สมัครจากรายการหลักเพื่อดึงชื่อพรรค (ในกรณีที่ stats ไม่มี party_name)
        const baseInfo = candidates.find((/** @type {any} */ c) => c.id === cand.candidate_id);
        return {
            ...cand,
            party_name: cand.party_name || baseInfo?.party || 'ไม่ระบุพรรค'
        };
    });

    return {
        stats: {
            ...stats,
            constituency_results: enrichedConstituencyResults
        },
        constituencies,
        selected_const: const_id
    };
}