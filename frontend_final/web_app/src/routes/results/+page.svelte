<script>
  import { goto } from "$app/navigation";
  /** @type {{ data: any }} */
  let { data } = $props();

  let stats = $derived(data.stats);
  let constituencies = $derived(data.constituencies);
  let selectedConst = $derived(data.selected_const || "");

  // ฟังก์ชันเปลี่ยนเขตเพื่อโหลดข้อมูลใหม่
  // @ts-ignore
  function handleFilter(e) {
    const value = e.target.value;
    const url = value ? `/results?const_id=${value}` : `/results`;
    goto(url, { keepFocus: true }); // นำทางไปยัง URL ใหม่เพื่อเรียก load() ใหม่
  }
</script>

<div class="container">
  <header class="results-header">
    <h2>ผลการเลือกตั้งประจำปี 2026</h2>
    <div class="filter-section">
      <label for="const-filter">เลือกมุมมองในเขต :</label>
      <select id="const-filter" value={selectedConst} onchange={handleFilter}>
        <option value="">ภาพรวมทั้งประเทศ</option>
        {#each constituencies as c}
          <option value={c.const_id}>
            {c.region_name} - เขตเลือกตั้งที่ {c.const_number}
          </option>
        {/each}
      </select>
    </div>
  </header>

  <div class="results-grid">
    <!-- ส่วนที่ 1: ส.ส. เขต (Constituency Results) -->
    <section class="result-card">
      <div class="card-title constituency">
        รายชื่อผู้สมัคร ส.ส. เขต (คะแนนสูงสุด)
      </div>
      <div class="list-container">
        {#each stats.constituency_results as cand, i}
          <div class="row">
            <div class="rank">{i + 1}</div>
            <div class="info">
              <!-- ✅ เช็กถ้าไม่มีชื่อผู้สมัคร ให้แสดงเป็นไม่ประสงค์ลงคะแนน -->
              <span class="name">{cand.full_name || "ไม่ประสงค์ลงคะแนน"}</span>
              {#if cand.candidate_id}
                <span class="party-sub"
                  >หมายเลขผู้สมัคร: {cand.candidate_id}</span
                >
                <span class="party-name">พรรค: {cand.party_name}</span>
              {:else}
                <span class="party-sub text-muted">คะแนนงดออกเสียง</span>
              {/if}
            </div>
            <div class="votes">
              <strong>{cand.votes.toLocaleString()}</strong>
              <span>คะแนน</span>
            </div>
          </div>
        {/each}
        {#if stats.constituency_results.length === 0}
          <p class="empty">ยังไม่มีข้อมูลคะแนน ส.ส. เขต</p>
        {/if}
      </div>
    </section>

    <!-- ส่วนที่ 2: ส.ส. พรรค (Party List Results) -->
    <section class="result-card">
      <div class="card-title party">คะแนนพรรคการเมือง (บัญชีรายชื่อ)</div>
      <div class="list-container">
        {#each stats.party_list_results as party, i}
          <div class="row">
            <div class="rank">{i + 1}</div>
            <div class="info">
              <span class="name">{party.party_name}</span>

              {#if party.party_id}
                <span class="party-sub">รหัสพรรค: {party.party_id}</span>
              {:else}
                <span class="party-sub text-muted">คะแนนงดออกเสียงพรรค</span>
              {/if}
            </div>

            <div class="votes">
              <strong>{party.votes.toLocaleString()}</strong>
              <span>คะแนน</span>
            </div>
          </div>
        {/each}
        {#if stats.party_list_results.length === 0}
          <p class="empty">ยังไม่มีข้อมูลคะแนนพรรคการเมือง</p>
        {/if}
      </div>
    </section>
  </div>
</div>

<style>
  .container {
    max-width: 1100px;
    margin: 30px auto;
    padding: 0 20px;
    font-family: "Sarabun", sans-serif;
  }

  .results-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    padding-bottom: 15px;
    border-bottom: 2px solid #e2e8f0;
  }

  .filter-section select {
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #cbd5e0;
    font-size: 1rem;
  }

  .results-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 30px;
  }
  @media (min-width: 850px) {
    .results-grid {
      grid-template-columns: 1fr 1fr;
    }
  }

  .result-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    overflow: hidden;
  }

  .card-title {
    padding: 15px;
    color: white;
    font-weight: bold;
    font-size: 1.1rem;
    text-align: center;
  }
  .card-title.constituency {
    background: #2b6cb0;
  }
  .card-title.party {
    background: #2f855a;
  }

  .list-container {
    padding: 10px;
  }

  .row {
    display: flex;
    align-items: center;
    padding: 15px;
    border-bottom: 1px solid #edf2f7;
    transition: background 0.2s;
  }
  .row:hover {
    background: #f7fafc;
  }

  .rank {
    width: 35px;
    font-weight: bold;
    color: #a0aec0;
    font-size: 1.2rem;
  }
  .info {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
  }
  .name {
    font-weight: bold;
    font-size: 1.05rem;
    color: #2d3748;
  }
  .party-sub {
    font-size: 0.8rem;
    color: #718096;
  }
  .party-name {
    font-size: 0.8rem;
    color: #718096;
  }

  .votes {
    text-align: right;
  }
  .votes strong {
    display: block;
    font-size: 1.2rem;
    color: #2d3748;
  }
  .votes span {
    font-size: 0.75rem;
    color: #a0aec0;
  }

  .empty {
    text-align: center;
    padding: 40px;
    color: #a0aec0;
  }
</style>
