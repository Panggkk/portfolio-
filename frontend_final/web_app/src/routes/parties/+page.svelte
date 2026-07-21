<script>
  //@ts-nocheck

  /** @type {{ data: any, form: any }} */
  let { data, form } = $props();
</script>

<div class="app-container">
  <header class="main-header">
    <div class="header-content">
      <h1>ระบบจัดการข้อมูลการเลือกตั้ง</h1>
      <p class="subtitle">
        จัดการรายชื่อพรรคและผู้สมัครรับเลือกตั้งสมาชิกสภาผู้แทนราษฎร
      </p>
    </div>
  </header>

  <main class="content-grid">
    <section class="admin-card">
      <div class="card-header">
        <h2>จัดการข้อมูลพรรคการเมือง</h2>
      </div>

      <div class="card-body">
        <form method="POST" action="?/createParty" class="vertical-form">
          <div class="form-grid">
            <div class="input-group">
              <label for="party_id">หมายเลขพรรค</label>
              <input
                type="number"
                name="party_id"
                placeholder="น้อยที่สุดคือ หมายเลข 1"
                min="1"
                required
              />
            </div>
            <div class="input-group">
              <label for="party_name">ชื่อพรรคการเมือง</label>
              <input
                type="text"
                name="party_name"
                placeholder="ระบุชื่อพรรค"
                required
              />
            </div>
            <div class="input-group">
              <label for="party_leader">ชื่อหัวหน้าพรรค</label>
              <input
                type="text"
                name="party_leader"
                placeholder="ชื่อ-นามสกุล"
                required
              />
            </div>
            <div class="input-group">
              <label for="party_logo_url">URL โลโก้ (ถ้ามี)</label>
              <input
                type="text"
                name="party_logo_url"
                placeholder="https://..."
              />
            </div>
          </div>
          <button type="submit" class="btn-primary"
            >ลงทะเบียนพรรคการเมืองใหม่</button
          >
        </form>

        {#if form?.success && form?.type === "party"}
          <div class="alert success">✅ บันทึกข้อมูลพรรคเรียบร้อยแล้ว</div>
        {/if}
        {#if form?.error && form?.type === "party"}
          <div class="alert error">❌ {form.error}</div>
        {/if}

        <div class="table-wrapper">
          <table class="data-table">
            <thead>
              <tr>
                <th class="w-80">เบอร์</th>
                <th>ชื่อพรรค</th>
                <th>หัวหน้าพรรค</th>
              </tr>
            </thead>
            <tbody>
              {#each data.parties as party}
                <tr>
                  <td><span class="id-badge">#{party.party_id}</span></td>
                  <td><span class="font-bold">{party.party_name}</span></td>
                  <td>{party.party_leader || "-"}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="admin-card">
      <div class="card-header">
        <h2>การจัดการผู้สมัคร ส.ส. เขต</h2>
      </div>

      <div class="card-body">
        <form method="POST" action="?/createCandidate" class="vertical-form">
          <div class="form-grid">
            <div class="input-group">
              <label for="full_name">ชื่อ-นามสกุลผู้สมัคร</label>
              <input
                type="text"
                name="full_name"
                placeholder="ระบุชื่อ-นามสกุล"
                required
              />
            </div>
            <div class="input-group">
              <label for="candidate_number">หมายเลขผู้สมัคร</label>
              <input
                type="number"
                name="candidate_number"
                placeholder="น้อยที่สุดคือเลข 1"
                min="1"
                required
              />
            </div>
            <div class="input-group">
              <label for="party_id">สังกัดพรรคการเมือง</label>
              <select name="party_id" required>
                <option value="">-- เลือกพรรค --</option>
                {#each data.parties as party}
                  <option value={party.party_id}
                    >{party.party_name} (#{party.party_id})</option
                  >
                {/each}
              </select>
            </div>
            <div class="input-group">
              <label for="const_id">เขตเลือกตั้ง</label>
              <select name="const_id" required>
                <option value="">-- เลือกเขต --</option>
                {#each data.constituencies as con}
                  <option value={con.const_id}
                    >เขต {con.const_number} ({con.region_name})</option
                  >
                {/each}
              </select>
            </div>
          </div>
          <button type="submit" class="btn-primary"
            >ลงทะเบียนผู้สมัครใหม่</button
          >
        </form>

        {#if form?.success && form?.type === "candidate"}
          <div class="alert success">✅ บันทึกข้อมูลผู้สมัครเรียบร้อยแล้ว</div>
        {/if}
        {#if form?.error && form?.type === "candidate"}
          <div class="alert error">❌ {form.error}</div>
        {/if}

        <div class="table-wrapper">
          <table class="data-table">
            <thead>
              <tr>
                <th class="w-80">เบอร์</th>
                <th>ชื่อผู้สมัคร</th>
                <th>พรรค</th>
                <th>พื้นที่</th>
              </tr>
            </thead>
            <tbody>
              {#each data.candidates as candidate}
                <tr>
                  <td
                    ><span class="num-badge">{candidate.candidate_number}</span
                    ></td
                  >
                  <td><span class="font-bold">{candidate.full_name}</span></td>
                  <td><span class="text-sm">{candidate.party}</span></td>
                  <td>
                    <div class="area-info">
                      <span class="text-xs">เขต {candidate.const_number}</span>
                      <span class="text-muted"
                        >{data.constituencies.find(
                          (c) => c.const_number === candidate.const_number,
                        )?.region_name || "ไม่พบข้อมูลจังหวัด"}</span
                      >
                    </div>
                  </td>
                </tr>
              {:else}
                <tr>
                  <td colspan="4" class="text-center py-20 text-muted"
                    >ไม่พบข้อมูลผู้สมัครในระบบ</td
                  >
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  </main>
</div>

<style>
  @import url("https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;600;700&display=swap");

  :global(body) {
    font-family: "Sarabun", sans-serif;
    background-color: #f1f5f9;
    color: #1e293b;
    margin: 0;
  }

  .app-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 40px 20px;
  }

  /* Header Section */
  .main-header {
    text-align: center;
    margin-bottom: 40px;
  }

  h1 {
    font-size: 2.5rem;
    color: #0f172a;
    margin: 0;
    letter-spacing: -0.5px;
  }

  .subtitle {
    color: #64748b;
    font-size: 1.1rem;
    margin-top: 10px;
  }

  /* Card Layout */
  .admin-card {
    background: white;
    border-radius: 16px;
    box-shadow:
      0 4px 6px -1px rgb(0 0 0 / 0.1),
      0 2px 4px -2px rgb(0 0 0 / 0.1);
    margin-bottom: 40px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
  }

  .card-header {
    background: #f8fafc;
    padding: 20px 30px;
    border-bottom: 1px solid #e2e8f0;
  }

  .card-header h2 {
    font-size: 1.25rem;
    margin: 0;
    color: #334155;
  }

  .card-body {
    padding: 30px;
  }

  /* Form Styling */
  .form-grid {
    display: grid;
    gap: 20px;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    margin-bottom: 25px;
  }

  .input-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .input-group label {
    font-size: 0.9rem;
    font-weight: 600;
    color: #475569;
  }

  input,
  select {
    padding: 12px 16px;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    font-size: 1rem;
    transition: all 0.2s;
    background-color: #ffffff;
  }

  input:focus,
  select:focus {
    outline: none;
    border-color: #6366f1;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
  }

  .btn-primary {
    background-color: #4f46e5;
    color: white;
    padding: 14px 24px;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    cursor: pointer;
    width: 100%;
    transition: background 0.2s;
  }

  .btn-primary:hover {
    background-color: #4338ca;
  }

  /* Table Styling */
  .table-wrapper {
    margin-top: 40px;
    overflow-x: auto;
  }

  .data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.95rem;
  }

  .data-table th {
    background: #f8fafc;
    padding: 16px;
    text-align: left;
    color: #64748b;
    font-weight: 600;
    border-bottom: 2px solid #f1f5f9;
  }

  .data-table td {
    padding: 16px;
    border-bottom: 1px solid #f1f5f9;
  }

  .data-table tr:hover {
    background-color: #f8fafc;
  }

  /* Badges & Info */
  .id-badge {
    background: #f1f5f9;
    color: #475569;
    padding: 4px 10px;
    border-radius: 6px;
    font-family: monospace;
    font-weight: bold;
  }

  .num-badge {
    background: #6366f1;
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: bold;
  }

  .area-info {
    display: flex;
    flex-direction: column;
  }

  .text-muted {
    color: #94a3b8;
  }
  .font-bold {
    font-weight: 700;
  }
  .text-sm {
    font-size: 0.85rem;
  }
  .text-xs {
    font-size: 0.75rem;
    font-weight: bold;
  }

  /* Alerts */
  .alert {
    padding: 16px;
    border-radius: 10px;
    margin-top: 20px;
    font-weight: 600;
    text-align: center;
  }

  .success {
    background: #dcfce7;
    color: #166534;
    border: 1px solid #bbf7d0;
  }
  .error {
    background: #fee2e2;
    color: #991b1b;
    border: 1px solid #fecaca;
  }

  .w-80 {
    width: 80px;
  }
  .py-20 {
    padding-top: 20px;
    padding-bottom: 20px;
  }
  .text-center {
    text-align: center;
  }
</style>
