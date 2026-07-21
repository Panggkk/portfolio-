<script>
  // ข้อมูลเมนูสำหรับเชื่อมไปยังหน้าต่าง ๆ
  const menus = [
    {
      href: "/parties",
      title: "จัดการข้อมูลพรรคการเมือง",
      desc: "เพิ่มและแสดงข้อมูลพรรคการเมือง ผู้สมัคร ส.ส. เขต และมีรายละเอียดของเขตเลือกตั้ง",
      color: "#2563eb",
    },
    {
      href: "/voters",
      title: "รายชื่อผู้มีสิทธิ",
      desc: "ตรวจสอบรายชื่อและสถานะการใช้สิทธิ รายชื่อผู้มีสิทธิ์เลือกตั้ง และรายละเอียดของเขตเลือกตั้ง",
      color: "#059669",
    },
    {
      href: "/voting",
      title: "บันทึกการลงคะแนน",
      desc: "ระบบบันทึกคะแนนเลือกตั้งแบบรายบุคคลไม่ระบุตัวตน และ แสดงจํานวนผู้ลงคะแนนแยกตามเขตเลือกตั้งทั้งแบบพรรค และ ส.ส.เขต ได้",
      color: "#0d9488",
    },
    {
      href: "/results",
      title: "รายงานผลการเลือกตั้ง",
      desc: "สรุปคะแนนผู้สมัครและพรรคการเมือง แสดงผลการเลือกตั้งแบบพรรคการเมือง และแบบ ส.ส. เขต แบบภาพรวม และแบบแยกตามเขต",
      color: "#1e3a8a",
    },
  ];
</script>

<div class="landing-container">
  <header class="hero">
    <h1>ระบบจัดการข้อมูลการเลือกตั้ง</h1>
  </header>

  <div class="menu-grid">
    {#each menus as menu}
      <a href={menu.href} class="menu-card">
        <div class="accent-bar" style="background-color: {menu.color}"></div>
        <div class="info">
          <h3>{menu.title}</h3>
          <p>{menu.desc}</p>
        </div>
        <div class="action-text">เข้าสู่หน้านี้</div>
      </a>
    {/each}
  </div>

  <footer class="footer">
    <p>Election Management System | 2026</p>
  </footer>
</div>

<style>
  .landing-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 40px 20px;
    font-family: "Sarabun", sans-serif;
  }

  .hero {
    text-align: center;
    margin-bottom: 60px;
  }

  .hero h1 {
    font-size: 2.2rem;
    color: #1e3a8a;
    font-weight: 700;
    margin-bottom: 12px;
  }

  .menu-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 25px;
  }

  .menu-card {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: white;
    padding: 30px;
    border-radius: 12px;
    text-decoration: none;
    color: inherit;
    border: 1px solid #e2e8f0;
    transition: all 0.25s ease;
    height: 160px;
    position: relative;
    overflow: hidden;
  }

  .accent-bar {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
  }

  .menu-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 20px rgba(0, 0, 0, 0.05);
    border-color: #cbd5e1;
  }

  .info h3 {
    margin: 0;
    font-size: 1.2rem;
    color: #1e293b;
    font-weight: 600;
  }

  .info p {
    margin: 10px 0 0;
    font-size: 0.9rem;
    color: #64748b;
    line-height: 1.5;
  }

  .action-text {
    font-size: 0.8rem;
    font-weight: bold;
    color: #2563eb;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 20px;
  }

  .footer {
    margin-top: 80px;
    text-align: center;
    color: #94a3b8;
    font-size: 0.8rem;
    border-top: 1px solid #f1f5f9;
    padding-top: 20px;
  }

  @media (max-width: 640px) {
    .hero h1 {
      font-size: 1.7rem;
    }
    .menu-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
