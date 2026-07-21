<script>
  /** @type {{ data: any, form: any }} */
  let { data, form } = $props();

  let citizenId = $state("");

  /** @type {any} */
  let voterInfo = $state(null);
  let selectedVoteType = $state("Constituency"); // ค่าเริ่มต้นคือเลือก ส.ส.เขต

  // กรองผู้สมัครเฉพาะเขต (ในตัวอย่างนี้ถ้าไม่ได้ระบุเขตจาก Voter จะแสดงทั้งหมด หรือคุณสามารถทำระบบ Search ได้)
  let candidates = $derived(() => data.candidates);
  let parties = $derived(() => data.parties);

  //เช็คข้อมูลผู้โหวต
  // @ts-ignore
  function checkVoter(e) {
    citizenId = e.target.value.trim();

    const found = data.voters.find(
      // @ts-ignore
      (v) => String(v.citizen_id) === String(citizenId),
    );

    voterInfo = found || null;
  }

  // ตัวแปรเช็กว่าประเภทที่เลือก "ลงไปหรือยัง"
  // let alreadyVoted = $derived.by(() => {
  //   if (!voterInfo) return false;
  //   if (selectedVoteType === "Constituency") return voterInfo.has_voted_const;
  //   if (selectedVoteType === "PartyList") return voterInfo.has_voted_list;
  //   return false;
  // });

  let alreadyVoted = $derived.by(() => {
    if (!voterInfo) return false;
    return selectedVoteType === "Constituency"
      ? voterInfo.has_voted_const
      : voterInfo.has_voted_list;
  });

  // กรองผู้สมัคร: เฉพาะผู้สมัครที่อยู่ "เขตเดียวกับผู้โหวต" เท่านั้น
  let filteredCandidates = $derived.by(() => {
    if (!voterInfo) return [];

    return data.candidates.filter(
      // @ts-ignore
      (c) => {
        return String(c.const_number) === String(voterInfo.const_number);
      },
    );
  });
</script>

<div class="container">
  <div class="card vote-card">
    <h2>บันทึกการลงคะแนนเสียง</h2>
    <p class="subtitle">ระบบบันทึกคะแนนแบบไม่ระบุตัวตน (Anonymous)</p>

    {#if form?.success}
      <div class="alert success shadow-lg">
        <div class="alert-content">
          <span class="icon">🎉</span>
          <div class="message-body">
            <strong>บันทึกการลงคะแนนสำเร็จ!</strong>
            <p>
              ระบบได้อัปเดตสถานะการใช้สิทธิของคุณเรียบร้อยแล้ว <a
                href="/voters"
                class="link-voter">ตรวจสอบที่นี่</a
              >
            </p>
            <hr class="divider" />
            <p class="hint">
              คุณสามารถตรวจสอบสถานะล่าสุดได้ที่หน้า
              <a href="/voters" class="link-voter">รายชื่อผู้มีสิทธิเลือกตั้ง</a
              >
            </p>
          </div>
        </div>
      </div>
    {/if}

    {#if form?.error}
      <div class="alert error">⚠️ {form.error}</div>
    {/if}

    <form method="POST" action="?/castVote ">
      <!-- ขั้นตอนที่ 1: ยืนยันตัวตน -->
      <div class="form-group">
        <label for="citizen_id">เลขบัตรประชาชน 13 หลักของผู้มีสิทธิ</label>
        <input
          type="text"
          name="citizen_id"
          bind:value={citizenId}
          maxlength="13"
          placeholder="13 หลัก"
          oninput={checkVoter}
          required
        />

        {#if voterInfo}
          <div class="info-badge {alreadyVoted ? 'voted-warning' : 'can-vote'}">
            <strong>{voterInfo.full_name}</strong> (เขต {voterInfo.const_number})
            <br />
            {#if alreadyVoted}
              <span class="text-danger">❌ ท่านใช้สิทธิในส่วนนี้ไปแล้ว</span>
            {:else}
              <span class="text-success">✅ ท่านมีสิทธิลงคะแนนในส่วนนี้</span>
            {/if}
          </div>
        {/if}

        {#if citizenId.length === 13 && !voterInfo}
          <div class="alert error">ไม่พบข้อมูลผู้มีสิทธิเลือกตั้ง</div>
        {/if}
      </div>

      <!-- ขั้นตอนที่ 2: เลือกประเภทการลงคะแนน -->
      <label for="select">เลือกประเภทการลงคะแนน ได้อย่างใดอย่างหนึ่ง</label>

      <div class="tab-group">
        <button
          type="button"
          class:active={selectedVoteType === "Constituency"}
          onclick={() => (selectedVoteType = "Constituency")}
          >เลือก ส.ส.เขต</button
        >
        <button
          type="button"
          class:active={selectedVoteType === "PartyList"}
          onclick={() => (selectedVoteType = "PartyList")}
          >เลือกพรรค (บัญชีรายชื่อ)</button
        >
      </div>
      <input type="hidden" name="vote_type" value={selectedVoteType} />

      <!-- ขั้นตอนที่ 3: เลือกตัวเลือก -->
      <div class="selection-area">
        {#if selectedVoteType === "Constituency"}
          <label for="candidate_id">เลือกผู้สมัคร (ส.ส.เขต)</label>
          <select name="candidate_id" required>
            <option value="">-- โปรดเลือกผู้สมัคร --</option>

            {#each filteredCandidates as c}
              <option value={c.id}
                >เบอร์ {c.candidate_number} : {c.full_name} ({c.party})</option
              >
            {/each}
          </select>
        {:else}
          <label for="party_id">เลือกพรรคการเมือง</label>
          <select name="party_id" required>
            <option value="">-- โปรดเลือกพรรค --</option>

            {#each data.parties as p}
              <option value={p.party_id}>{p.party_name}</option>
            {/each}
          </select>
        {/if}
      </div>

      <button
        type="submit"
        class="btn-vote"
        disabled={!voterInfo || alreadyVoted}
      >
        {alreadyVoted ? "ท่านใช้สิทธินี้ไปแล้ว" : "ยืนยันการลงคะแนน"}
      </button>
    </form>
  </div>

  <div class="card turnout-card mt-30">
    <div class="turnout-header">
      <h3>สรุปจำนวนผู้มาใช้สิทธิ</h3>
    </div>
    <p class="table-subtitle">ข้อมูลแยกตามเขตเลือกตั้งและประเภทบัตร</p>

    <div class="table-responsive">
      <table class="styled-table">
        <thead>
          <tr>
            <th>ภูมิภาค/จังหวัด</th>
            <th>เขต</th>
            <th class="center">ส.ส.เขต (คน)</th>
            <th class="center">ส.ส.พรรค (คน)</th>
          </tr>
        </thead>
        <tbody>
          {#each data.turnout_report as t}
            <tr>
              <td class="region-cell">{t.region_name}</td>
              <td><span class="const-badge">เขต {t.const_number}</span></td>
              <td class="center count-cell blue-text"
                >{t.const_count.toLocaleString()}</td
              >
              <td class="center count-cell green-text"
                >{t.party_count.toLocaleString()}</td
              >
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </div>
</div>

<style>
  .container {
    max-width: 900px;
    margin: 50px auto;
    font-family: "Sarabun", sans-serif;
  }
  .card {
    background: white;
    padding: 40px;
    border-radius: 15px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  }
  h2 {
    color: #1e3a8a;
    text-align: center;
    margin-bottom: 5px;
  }
  .subtitle {
    text-align: center;
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 30px;
  }
  .form-group {
    margin-bottom: 20px;
  }
  label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
  }
  input,
  select {
    width: 100%;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 1rem;
  }
  .tab-group {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
  }
  .tab-group button {
    flex: 1;
    padding: 10px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    background: #eee;
  }
  .tab-group button.active {
    background: #1e3a8a;
    color: white;
  }
  .btn-vote {
    width: 100%;
    background: #059669;
    color: white;
    border: none;
    padding: 15px;
    border-radius: 8px;
    font-size: 1.1rem;
    font-weight: bold;
    cursor: pointer;
    margin-top: 20px;
  }
  .alert {
    margin-top: 25px;
    padding: 20px;
    border-radius: 12px;
    border-left: 6px solid;
    animation: slideUp 0.4s ease-out;
  }
  .error {
    background-color: #fef2f2;
    color: #991b1b;
    border-color: #ef4444;
  }
  .success {
    background-color: #f0fdf4;
    color: #166534;
    border-color: #22c55e;
  }

  .alert-content {
    display: flex;
    gap: 15px;
    align-items: flex-start;
  }

  .icon {
    font-size: 1.5rem;
  }

  .message-body strong {
    display: block;
    font-size: 1.1rem;
    margin-bottom: 5px;
  }

  .divider {
    border: 0;
    border-top: 1px solid #bbf7d0;
    margin: 12px 0;
  }

  .hint {
    font-size: 0.9rem;
    margin: 0;
  }

  .link-voter {
    color: #15803d;
    font-weight: bold;
    text-decoration: underline;
  }

  .link-voter:hover {
    color: #166534;
  }

  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .shadow-lg {
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  }

  .info-badge {
    margin-top: 10px;
    padding: 10px;
    border-radius: 8px;
    font-size: 0.9rem;
    border: 1px solid #ddd;
  }
  .voted-warning {
    background-color: #fff5f5;
    border-color: #feb2b2;
  }
  .can-vote {
    background-color: #f0fff4;
    border-color: #9ae6b4;
  }
  .text-danger {
    color: #c53030;
    font-weight: bold;
  }
  .text-success {
    color: #2f855a;
    font-weight: bold;
  }

  .btn-vote:disabled {
    background-color: #a0aec0;
    cursor: not-allowed;
    opacity: 0.7;
  }

  select:disabled {
    background-color: #edf2f7;
    cursor: not-allowed;
  }

  /* ระยะห่างการ์ดล่าง */
  .mt-30 {
    margin-top: 30px;
  }

  /* หัวข้อรายงาน */
  .turnout-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    border-left: 4px solid #1e3a8a;
    padding-left: 12px;
  }

  .turnout-header h3 {
    margin: 0;
    color: #1e3a8a;
    font-size: 1.1rem;
    font-weight: 600;
  }

  /* ตาราง - ตัดขอบและเงาที่เกินจำเป็น */
  .table-responsive {
    overflow-x: auto;
    border-top: 1px solid #eee;
  }

  .styled-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
  }

  .styled-table th {
    background-color: #fafafa;
    color: #666;
    font-weight: 600;
    text-align: left;
    padding: 12px;
    border-bottom: 1px solid #eee;
  }

  .styled-table td {
    padding: 12px;
    border-bottom: 1px solid #f9f9f9;
    color: #444;
  }

  /* Hover แค่พอให้รู้ว่าเม้าส์ชี้ */
  .styled-table tbody tr:hover {
    background-color: #fcfcfc;
  }

  /* Badge เขต - ทำให้เรียบที่สุด */
  .const-badge {
    color: #666;
    font-size: 0.85rem;
  }

  /* ตัวเลขคะแนน - เน้นแค่ความหนาและสี */
  .count-cell {
    font-weight: 600;
  }

  .center {
    text-align: center;
  }
  .blue-text {
    color: #2563eb;
  }
  .green-text {
    color: #059669;
  }

  /* Mobile */
  @media (max-width: 480px) {
    .styled-table th,
    .styled-table td {
      padding: 10px 8px;
      font-size: 0.8rem;
    }
  }
</style>
