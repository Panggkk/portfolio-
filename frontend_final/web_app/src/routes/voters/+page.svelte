<script>
  /** @type {{ data: any, form: any }} */
  let { data, form } = $props();
</script>

<div class="container">
  <header class="header">
    <h2>จัดการรายชื่อผู้มีสิทธิเลือกตั้ง</h2>
    <p>ระบบตรวจสอบและลงทะเบียนรายชื่อผู้มีสิทธิเลือกตั้งประจำปี 2026</p>
  </header>

  <div class="grid-layout">
    <!-- ส่วนของ Form เพิ่มรายชื่อ -->
    <section class="card form-section">
      <div class="card-header">
        <h3>เพิ่มรายชื่อ ผู้มีสิทธิเลือกตั้ง</h3>
      </div>
      <form method="POST" action="?/addVoter" class="voter-form">
        <div class="input-group">
          <label for="citizen_id">เลขบัตรประชาชน</label>
          <input
            type="text"
            id="citizen_id"
            name="citizen_id"
            placeholder="1-XXXX-XXXXX-XX-X"
            required
            maxlength="13"
          />
        </div>

        <div class="input-group">
          <label for="full_name">ชื่อ-นามสกุล</label>
          <input
            type="text"
            id="full_name"
            name="full_name"
            placeholder="ชื่อจริง - นามสกุล"
            required
          />
        </div>

        <div class="input-group">
          <label for="const_id">เขตเลือกตั้ง</label>
          <select name="const_id" id="const_id" required>
            <option value="">-- โปรดเลือกเขตเลือกตั้ง --</option>
            {#each data.constituencies as c}
              <option value={c.const_id}>
                {c.region_name} - เขตที่ {c.const_number}
              </option>
            {/each}
          </select>
        </div>

        <button type="submit" class="btn-primary">ลงทะเบียนผู้มีสิทธิ</button>
      </form>

      {#if form?.error}
        <div class="alert alert-error">
          <span>⚠️ {form.message}</span>
        </div>
      {/if}
      {#if form?.success}
        <div class="alert alert-success">
          <span>✅ ลงทะเบียนสำเร็จเรียบร้อยแล้ว</span>
        </div>
      {/if}
    </section>

    <!-- ส่วนแสดงตารางรายชื่อ -->
    <section class="card table-section">
      <div class="card-header">
        <h3>รายชื่อผู้มีสิทธิในระบบ</h3>
      </div>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>ชื่อ-นามสกุล</th>
              <th>เลขบัตรประชาชน</th>
              <th>จังหวัด</th>
              <th>เขตที่</th>
              <th class="center">สส.เขต</th>
              <th class="center">สส.พรรค</th>
            </tr>
          </thead>
          <tbody>
            {#each data.voters as v}
              <tr>
                <td class="font-bold">{v.full_name}</td>
                <td class="mono">{v.citizen_id}</td>
                <td>{v.region_name}</td>
                <td><span class="badge-info">เขต {v.const_number}</span></td>
                <td class="center">
                  <span
                    class="status-badge {v.has_voted_const
                      ? 'voted'
                      : 'not-voted'}"
                  >
                    {v.has_voted_const ? "ลงคะแนนแล้ว" : "ยังไม่ได้ใช้สิทธิ"}
                  </span>
                </td>
                <td class="center">
                  <span
                    class="status-badge {v.has_voted_list
                      ? 'voted'
                      : 'not-voted'}"
                  >
                    {v.has_voted_list ? "ลงคะแนนแล้ว" : "ยังไม่ได้ใช้สิทธิ"}
                  </span>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </section>
  </div>
</div>

<style>
  :global(body) {
    background-color: #f4f7f9;
    color: #333;
    margin: 0;
  }

  .container {
    max-width: 1200px;
    margin: 40px auto;
    padding: 0 20px;
    font-family: "Sarabun", sans-serif;
  }

  .header {
    text-align: center;
    margin-bottom: 40px;
  }

  .header h2 {
    color: #1a365d;
    margin-bottom: 8px;
    font-size: 2rem;
  }

  .grid-layout {
    display: grid;
    grid-template-columns: 1fr;
    gap: 30px;
  }

  @media (min-width: 992px) {
    .grid-layout {
      grid-template-columns: 350px 1fr;
    }
  }

  /* Card Style */
  .card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    height: fit-content;
  }

  .card-header {
    background-color: #1a365d;
    color: white;
    padding: 15px 20px;
  }

  .card-header h3 {
    margin: 0;
    font-size: 1.1rem;
  }

  /* Form Style */
  .voter-form {
    padding: 20px;
  }

  .input-group {
    margin-bottom: 15px;
  }

  .input-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: 600;
    font-size: 0.9rem;
  }

  input,
  select {
    width: 100%;
    padding: 10px;
    border: 1px solid #cbd5e0;
    border-radius: 6px;
    box-sizing: border-box;
    font-size: 1rem;
    transition: border-color 0.2s;
  }

  input:focus,
  select:focus {
    outline: none;
    border-color: #4299e1;
    box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2);
  }

  .btn-primary {
    width: 100%;
    background-color: #2b6cb0;
    color: white;
    border: none;
    padding: 12px;
    border-radius: 6px;
    font-weight: bold;
    cursor: pointer;
    transition: background 0.2s;
    margin-top: 10px;
  }

  .btn-primary:hover {
    background-color: #2c5282;
  }

  /* Table Style */
  .table-container {
    overflow-x: auto;
  }

  table {
    width: 100%;
    border-collapse: collapse;
  }

  th {
    background-color: #edf2f7;
    padding: 15px;
    text-align: left;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #4a5568;
  }

  td {
    padding: 15px;
    border-bottom: 1px solid #edf2f7;
    font-size: 0.95rem;
  }

  .center {
    text-align: center;
  }
  .font-bold {
    font-weight: bold;
  }
  .mono {
    font-family: "Courier New", monospace;
    letter-spacing: 1px;
  }

  /* Badges & Alerts */
  .status-badge {
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
  }

  .status-badge.voted {
    background: #c6f6d5;
    color: #22543d;
  }
  .status-badge.not-voted {
    background: #fed7d7;
    color: #822727;
  }

  .badge-info {
    background: #ebf8ff;
    color: #2b6cb0;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.85rem;
  }

  .alert {
    margin: 15px 20px;
    padding: 12px;
    border-radius: 6px;
    font-size: 0.9rem;
  }

  .alert-error {
    background-color: #fff5f5;
    color: #c53030;
    border-left: 4px solid #c53030;
  }
  .alert-success {
    background-color: #f0fff4;
    color: #2f855a;
    border-left: 4px solid #48bb78;
  }
</style>
