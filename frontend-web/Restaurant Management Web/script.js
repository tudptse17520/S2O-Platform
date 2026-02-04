/* =========================================
   1. KHỞI TẠO DỮ LIỆU MẪU (DATABASE)
   ========================================= */
// Thêm biến này vào phần khai báo biến toàn cục (đầu file JS)
let currentTableArea = "all";
// Dữ liệu Món ăn
let menuData = {
  "pho-bo": {
    title: "Phở Anh Hai",
    price: 45000,
    img: "https://cdn-media.sforum.vn/storage/app/media/phuonganh/cach-tai-game-tiem-pho-cua-anh-hai.jpg",
    desc: "Hương vị truyền thống với nước dùng ninh từ xương ống trong 24h, thảo quả, quế hồi. Thịt bò tái nạm mềm ngọt, bánh phở tươi.",
    isAvailable: true,
  },
  "ga-chien": {
    title: "Gà Chiên Mắm Tỏi",
    price: 120000,
    img: "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?q=80&w=800&auto=format&fit=crop",
    desc: "Gà ta thả vườn chắc thịt, chiên giòn da và sốt nước mắm tỏi ớt đậm đà.",
    isAvailable: true,
  },
  "lau-thai": {
    title: "Lẩu Thái Hải Sản",
    price: 250000,
    img: "https://cdn2.fptshop.com.vn/unsafe/Uploads/images/tin-tuc/173437/Originals/cach-nau-lau-thai-hai-san-chua-cay-5.jpg",
    desc: "Nồi lẩu chua cay chuẩn vị Thái với tôm sú, mực ống, nghêu, cá phi lê.",
    isAvailable: true,
  },
  "nom-sua": {
    title: "Nộm Sứa Biển",
    price: 65000,
    img: "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?q=80&w=800&auto=format&fit=crop",
    desc: "Sứa biển tươi giòn sần sật, trộn cùng xoài xanh, cà rốt, rau thơm.",
    isAvailable: true,
  },
  "com-chien": {
    title: "Cơm Chiên Dương Châu",
    price: 50000,
    img: "https://daotaobeptruong.vn/wp-content/uploads/2021/02/ban-com-chien-duong-chau.jpg",
    desc: "Cơm chiên hạt vàng óng, tơi xốp, kết hợp với lạp xưởng.",
    isAvailable: true,
  },
  bia: {
    title: "Bia & Đồ Uống",
    price: 15000,
    img: "https://images.unsplash.com/photo-1608270586620-248524c67de9?q=80&w=800&auto=format&fit=crop",
    desc: "Đa dạng các loại bia chai và nước ngọt các loại.",
    isAvailable: true,
  },
};

// Dữ liệu Khuyến mãi
const promotions = {
  GIAM10: 0.1, // Giảm 10%
  VIP20: 0.2, // Giảm 20%
  KHAIMO: 0.5, // Giảm 50%
};

// Dữ liệu Bàn (Kèm lịch sử và order chi tiết)
let tableData = [
  {
    id: 1,
    name: "Bàn 01",
    area: "Tầng 1",
    status: "empty",
    orders: [],
    history: [],
  },
  {
    id: 2,
    name: "Bàn 02",
    area: "Tầng 1",
    status: "occupied",
    timeIn: "10:30",
    orders: [
      {
        name: "Lẩu Thái Hải Sản",
        price: 250000,
        qty: 1,
        note: "Ít cay",
        status: "cooking",
      },
      {
        name: "Bia Hà Nội",
        price: 15000,
        qty: 5,
        note: "Lạnh",
        status: "served",
      },
    ],
    history: [],
  },
  {
    id: 3,
    name: "Bàn 03",
    area: "Tầng 1",
    status: "empty",
    orders: [],
    history: [],
  },
  {
    id: 4,
    name: "Bàn 04",
    area: "Tầng 1",
    status: "reserved",
    orders: [],
    history: [],
  },
  {
    id: 5,
    name: "Bàn 05",
    area: "Tầng 2",
    status: "empty",
    orders: [],
    history: [],
  },
  {
    id: 6,
    name: "Bàn 06",
    area: "Tầng 2",
    status: "occupied",
    orders: [],
    history: [],
  },
  {
    id: 7,
    name: "Bàn 07",
    area: "Tầng 2",
    status: "empty",
    orders: [],
    history: [],
  },
  {
    id: 8,
    name: "Bàn VIP 1",
    area: "Tầng 3",
    status: "empty",
    orders: [],
    history: [],
  },
  {
    id: 9,
    name: "Bàn VIP 2",
    area: "Tầng 3",
    status: "occupied",
    orders: [],
    history: [],
  },
];

// Dữ liệu Đơn hàng
let ordersData = [
  {
    id: 101,
    table: "Bàn 02",
    time: "10:30",
    total: "295.000đ",
    status: "pending",
    items: [
      { name: "Lẩu Thái", qty: 1, price: "250k" },
      { name: "Bia", qty: 3, price: "45k" },
    ],
  },
  {
    id: 102,
    table: "Bàn 06",
    time: "11:15",
    total: "120.000đ",
    status: "completed",
    items: [{ name: "Gà Chiên", qty: 1, price: "120k" }],
  },
  {
    id: 103,
    table: "Mang về",
    time: "11:20",
    total: "45.000đ",
    status: "pending",
    items: [{ name: "Phở Bò", qty: 1, price: "45k" }],
  },
  {
    id: 104,
    table: "Bàn VIP 2",
    time: "11:45",
    total: "565.000đ",
    status: "pending",
    items: [
      { name: "Lẩu Thái", qty: 2, price: "500k" },
      { name: "Nộm Sứa", qty: 1, price: "65k" },
    ],
  },
];

// Dữ liệu Nhân viên
let staffData = [
  {
    id: 1,
    name: "Đoàn Phạm Thanh Tú",
    role: "Phục vụ",
    status: "online",
    img: "https://maunailxinh.com/wp-content/uploads/2025/06/avatar-an-danh-1.jpg",
    info: { phone: "0901.234.567", dob: "1998", address: "Hà Nội" },
    schedule: "Ca Sáng (8:00 - 16:00) | T2 - T7",
    salary: { basic: "6.000.000", bonus: "500.000", total: "6.500.000" },
  },
  {
    id: 2,
    name: "Trần Ngọc Khánh Linh",
    role: "Thu ngân",
    status: "online",
    img: "https://maunailxinh.com/wp-content/uploads/2025/06/avatar-an-danh-1.jpg",
    info: { phone: "0912.345.678", dob: "1995", address: "Đà Nẵng" },
    schedule: "Ca Full (9:00 - 21:00) | T2 - T6",
    salary: { basic: "8.000.000", bonus: "1.000.000", total: "9.000.000" },
  },
  {
    id: 3,
    name: "Trần Đức Trung",
    role: "Đầu bếp",
    status: "offline",
    img: "https://maunailxinh.com/wp-content/uploads/2025/06/avatar-an-danh-1.jpg",
    info: { phone: "0987.654.321", dob: "1990", address: "HCM" },
    schedule: "Ca Gãy (10:00 - 14:00 & 17:00 - 22:00)",
    salary: { basic: "12.000.000", bonus: "2.000.000", total: "14.000.000" },
  },
  {
    id: 4,
    name: "Trần Chí Trung",
    role: "Bảo vệ",
    status: "online",
    img: "https://maunailxinh.com/wp-content/uploads/2025/06/avatar-an-danh-1.jpg",
    info: { phone: "0345.678.901", dob: "1985", address: "Hải Phòng" },
    schedule: "Ca Đêm (20:00 - 6:00) | T2 - CN",
    salary: { basic: "7.000.000", bonus: "300.000", total: "7.300.000" },
  },
];
// --- DỮ LIỆU BIỂU ĐỒ (Cập nhật số liệu để test) ---
const chartData = {
  revenue: [
    { label: "Tiền mặt", value: 33, color: "#3b82f6", info: "5.200k" },
    { label: "CK", value: 53, color: "#ec4899", info: "8.500k" },
    { label: "Thẻ", value: 14, color: "#8b5cf6", info: "2.100k" },
  ],
  table: [
    { label: "Trống", value: 50, color: "#10b981", info: "12 bàn" },
    { label: "Có khách", value: 33, color: "#ec4899", info: "8 bàn" },
    { label: "Đặt trước", value: 17, color: "#3b82f6", info: "4 bàn" },
  ],
  order: [
    { label: "Tại bàn", value: 60, color: "#3b82f6", info: "45 đơn" },
    { label: "Mang về", value: 16, color: "#ec4899", info: "12 đơn" },
    { label: "App", value: 24, color: "#8b5cf6", info: "18 đơn" },
  ],
};
// --- HÀM VẼ BIỂU ĐỒ SVG (CÓ ĐƯỜNG KẺ CHỈ DẪN) ---
function drawDonutChart(containerId, data, centerText) {
  const container = document.getElementById(containerId);
  if (!container) return;

  // Cấu hình kích thước (Tăng size lên để có chỗ cho đường kẻ)
  const size = 240;
  const cx = size / 2;
  const cy = size / 2;
  const radius = 60; // Bán kính vòng tròn chính
  const labelRadius = 95; // Khoảng cách đẩy chữ ra xa (để nối dây)

  let currentAngle = -0.5 * Math.PI; // Bắt đầu từ 12 giờ

  // Tạo thẻ SVG với overflow visible
  let svgHtml = `<svg width="100%" height="100%" viewBox="0 0 ${size} ${size}" style="overflow: visible;">`;

  data.forEach((item) => {
    // 1. Tính toán góc
    const sliceAngle = (item.value / 100) * 2 * Math.PI;
    const endAngle = currentAngle + sliceAngle;

    // Tọa độ vẽ hình quạt
    const x1 = cx + radius * Math.cos(currentAngle);
    const y1 = cy + radius * Math.sin(currentAngle);
    const x2 = cx + radius * Math.cos(endAngle);
    const y2 = cy + radius * Math.sin(endAngle);

    const largeArcFlag = sliceAngle > Math.PI ? 1 : 0;
    const pathData = `M ${cx} ${cy} L ${x1} ${y1} A ${radius} ${radius} 0 ${largeArcFlag} 1 ${x2} ${y2} Z`;

    // 2. Tính toán vị trí đường kẻ chỉ dẫn
    const midAngle = currentAngle + sliceAngle / 2;

    // Điểm bắt đầu (trên vành tròn)
    const lx1 = cx + radius * Math.cos(midAngle);
    const ly1 = cy + radius * Math.sin(midAngle);

    // Điểm bẻ góc (ra xa một chút)
    const lx2 = cx + (labelRadius - 15) * Math.cos(midAngle);
    const ly2 = cy + (labelRadius - 15) * Math.sin(midAngle);

    // Điểm kết thúc (nơi hiện chữ)
    const lx3 = cx + labelRadius * Math.cos(midAngle);
    const ly3 = cy + labelRadius * Math.sin(midAngle);

    // Group chứa tất cả để xử lý hover chung
    svgHtml += `
        <g class="chart-group">
            <path d="${pathData}" fill="${
      item.color
    }" class="chart-segment"></path>
            
            <polyline points="${lx1},${ly1} ${lx2},${ly2} ${lx3},${ly3}" class="chart-line" />
            
            <circle cx="${lx3}" cy="${ly3}" r="2" class="chart-point" />

            <rect x="${lx3 - 40}" y="${
      ly3 - 20
    }" width="80" height="35" rx="4" class="chart-text-bg" />

            <text x="${lx3}" y="${ly3 - 5}" class="chart-text">${
      item.label
    }</text>
            <text x="${lx3}" y="${ly3 + 10}" class="chart-sub-text">${
      item.info
    }</text>
        </g>`;

    currentAngle += sliceAngle;
  });

  // Vẽ lỗ tròn trắng ở giữa
  svgHtml += `<circle cx="${cx}" cy="${cy}" r="${
    radius * 0.65
  }" fill="white" />`;
  svgHtml += `</svg>`;

  // Thêm chữ tổng ở giữa bằng HTML (dễ chỉnh style hơn SVG text)
  const centerLabel = `<div class="center-label">${centerText}</div>`;

  container.innerHTML = svgHtml + centerLabel;
}
// ... (Giữ nguyên phần init window.onload gọi hàm này) ...
// Biến toàn cục
let notifications = [];
let currentDishId = null,
  currentTableId = null,
  currentOrderId = null;
let isEditing = false,
  isAddingNew = false,
  isEditingStaff = false,
  currentStaffId = null;

// --- 2. HÀM ĐIỀU HƯỚNG (NAVIGATION) ---
function switchView(viewId) {
  document
    .querySelectorAll('[id^="view-"]')
    .forEach((el) => (el.style.display = "none"));
  document
    .querySelectorAll(".menu-item")
    .forEach((el) => el.classList.remove("active"));
  document.getElementById("view-" + viewId).style.display = "block";

  const navItem = document.getElementById("nav-" + viewId);
  if (navItem) navItem.classList.add("active");

  const titles = {
    dashboard: "Tổng quan kinh doanh",
    menu: "Quản lý thực đơn",
    tables: "Quản lý bàn & QR",
    orders: "Quản lý đơn hàng",
    staff: "Quản lý nhân viên",
  };
  document.getElementById("page-header-title").innerText =
    titles[viewId] || "Hệ thống quản lý";

  if (viewId === "orders") renderOrders();
  if (viewId === "staff") renderStaff();
  if (viewId === "tables") renderTables(); // Render lại bàn khi chuyển tab
}

// --- 3. QUẢN LÝ MENU (THÊM, SỬA, XÓA, UPLOAD) ---
function renderMenu() {
  const grid = document.getElementById("menu-grid-container");
  grid.innerHTML = "";

  for (const [id, dish] of Object.entries(menuData)) {
    // TÍNH TOÁN GIÁ
    let priceDisplay = "";

    if (currentMenuDiscount > 0) {
      // Nếu có mã giảm giá hợp lệ
      const discountedPrice = dish.price * (1 - currentMenuDiscount / 100);
      priceDisplay = `
            <div class="price-tag" style="display:flex; flex-direction:column; align-items:center;">
                <span style="font-size: 0.9rem; text-decoration: line-through; color: #94a3b8;">
                    ${dish.price.toLocaleString("vi-VN")}đ
                </span>
                <span style="color: #ef4444; font-size: 1.2rem;">
                    ${discountedPrice.toLocaleString("vi-VN")}đ
                    <small style="font-size:0.7rem; background:#fee2e2; padding:2px 5px; border-radius:4px;">-${currentMenuDiscount}%</small>
                </span>
            </div>
        `;
    } else {
      // Giá gốc bình thường
      priceDisplay = `<div class="price-tag">${dish.price.toLocaleString(
        "vi-VN"
      )}đ</div>`;
    }

    const dishCard = `
            <div class="menu-card" onclick="showDishDetail('${id}')">
                <img src="${dish.img}" class="menu-img" onerror="this.src='https://via.placeholder.com/300?text=No+Image'">
                <div class="menu-info">
                    <h4>${dish.title}</h4>
                    ${priceDisplay}
                </div>
            </div>`;
    grid.innerHTML += dishCard;
  }
}

document
  .getElementById("edit-img-file")
  .addEventListener("change", function (e) {
    if (e.target.files[0]) {
      const r = new FileReader();
      r.onload = function (ev) {
        document.getElementById("modal-img").src = ev.target.result;
        document.getElementById("edit-img-input").value = "";
      };
      r.readAsDataURL(e.target.files[0]);
    }
  });

function openAddModal() {
  isEditing = true;
  isAddingNew = true;
  currentDishId = null;
  document.getElementById("dishModal").style.display = "block";
  document.getElementById("modal-img").src =
    "https://via.placeholder.com/400x400?text=Anh+Mon+An";
  document.getElementById("img-input-container").style.display = "block";
  document.getElementById("edit-img-input").value = "";
  document.getElementById("edit-img-file").value = "";

  document.getElementById(
    "modal-title-container"
  ).innerHTML = `<input type="text" id="edit-title-input" class="edit-input" placeholder="Tên món..." style="font-size: 1.5rem;">`;
  document.getElementById(
    "modal-price-container"
  ).innerHTML = `<input type="text" id="edit-price-input" class="edit-input" placeholder="Giá tiền...">`;
  document.getElementById(
    "modal-desc-container"
  ).innerHTML = `<textarea id="edit-desc-input" class="edit-textarea" placeholder="Mô tả món ăn..."></textarea>`;

  document.getElementById("btn-toggle-status").style.display = "none";
  document.getElementById("delete-btn").style.display = "none";
  document.getElementById("modal-status").innerHTML = "● Đang tạo mới";
  document.getElementById("modal-status").className = "text-blue";
  document.getElementById("edit-btn-text").innerText = "Lưu món mới";
  document.getElementById("edit-btn").style.background = "#10b981";
}

function showDishDetail(id) {
  isEditing = false;
  isAddingNew = false;
  resetEditButton();
  const dish = menuData[id];
  currentDishId = id;

  if (dish) {
    document.getElementById(
      "modal-title-container"
    ).innerHTML = `<h2 id="modal-title" class="modal-title">${dish.title}</h2>`;
    document.getElementById(
      "modal-price-container"
    ).innerHTML = `<span id="modal-price" class="modal-price">${dish.price.toLocaleString(
      "vi-VN"
    )}đ</span>`;
    document.getElementById(
      "modal-desc-container"
    ).innerHTML = `<p id="modal-desc" class="modal-desc">${dish.desc}</p>`;
    document.getElementById("modal-img").src = dish.img;
    document.getElementById("img-input-container").style.display = "none";
    document.getElementById("btn-toggle-status").style.display = "inline-block";
    document.getElementById("delete-btn").style.display = "flex";
    updateStatusUI(dish.isAvailable);
    document.getElementById("dishModal").style.display = "block";
  }
}

function toggleEditMode() {
  const btnText = document.getElementById("edit-btn-text");
  if (isEditing) {
    const newTitle = document.getElementById("edit-title-input").value;
    const newPrice = document.getElementById("edit-price-input").value;
    const newDesc = document.getElementById("edit-desc-input").value;
    const newImg = document.getElementById("modal-img").src;

    if (!newTitle || !newPrice) {
      alert("Vui lòng nhập tên và giá món!");
      return;
    }

    if (isAddingNew) {
      const newId = "dish-" + Date.now();
      menuData[newId] = {
        title: newTitle,
        price: parseInt(newPrice),
        img: newImg,
        desc: newDesc,
        isAvailable: true,
      };
      addNotification(`Đã thêm món mới: <b>${newTitle}</b>`, "add");
    } else {
      menuData[currentDishId].title = newTitle;
      menuData[currentDishId].price = parseInt(newPrice);
      menuData[currentDishId].desc = newDesc;
      menuData[currentDishId].img = newImg;
      addNotification(`Đã cập nhật thông tin món: <b>${newTitle}</b>`, "info");
    }

    renderMenu();
    if (isAddingNew) closeModal("dishModal");
    else showDishDetail(currentDishId);
    isEditing = false;
    isAddingNew = false;
  } else {
    const currentDish = menuData[currentDishId];
    document.getElementById(
      "modal-title-container"
    ).innerHTML = `<input type="text" id="edit-title-input" class="edit-input" value="${currentDish.title}" style="font-size: 1.5rem; font-weight: bold;">`;
    document.getElementById(
      "modal-price-container"
    ).innerHTML = `<input type="text" id="edit-price-input" class="edit-input" value="${currentDish.price}">`;
    document.getElementById(
      "modal-desc-container"
    ).innerHTML = `<textarea id="edit-desc-input" class="edit-textarea">${currentDish.desc}</textarea>`;
    document.getElementById("img-input-container").style.display = "block";
    document.getElementById("edit-img-input").value = "";
    btnText.innerText = "Lưu thay đổi";
    document.getElementById("edit-btn").style.background = "#10b981";
    isEditing = true;
  }
}

function deleteDish() {
  if (confirm("Bạn có chắc chắn muốn xóa món này không?")) {
    delete menuData[currentDishId];
    renderMenu();
    closeModal("dishModal");
    addNotification(`Đã xóa món`, "delete");
  }
}

function toggleStatus() {
  if (menuData[currentDishId]) {
    menuData[currentDishId].isAvailable = !menuData[currentDishId].isAvailable;
    updateStatusUI(menuData[currentDishId].isAvailable);
    addNotification("Đã đổi trạng thái món", "status");
  }
}

function updateStatusUI(isAvailable) {
  const statusLabel = document.getElementById("modal-status");
  if (isAvailable) {
    statusLabel.innerHTML = "● Còn món";
    statusLabel.className = "text-green";
  } else {
    statusLabel.innerHTML = "● Hết món";
    statusLabel.className = "text-red";
  }
}

function resetEditButton() {
  document.getElementById("edit-btn-text").innerText = "Chỉnh sửa thông tin";
  document.getElementById("edit-btn").style.background = "";
}

// --- CẬP NHẬT: Hàm renderTables thông minh hơn (kết hợp lọc Tầng + Tìm món) ---
function renderTables() {
  const grid = document.getElementById("table-grid-container");
  grid.innerHTML = "";

  // 1. Lấy từ khóa tìm kiếm
  const searchInput = document.getElementById("table-dish-search");
  const keyword = searchInput ? searchInput.value.toLowerCase().trim() : "";

  // 2. Duyệt qua dữ liệu bàn
  tableData.forEach((t) => {
    // Điều kiện 1: Lọc theo khu vực (Tầng)
    if (currentTableArea !== "all" && t.area !== currentTableArea) return;

    // Điều kiện 2: Lọc theo tên món ăn (nếu có nhập từ khóa)
    // Logic: Nếu đang tìm kiếm, chỉ hiện bàn nào CÓ món đó trong orders
    if (keyword !== "") {
      const hasDish = t.orders.some((order) =>
        order.name.toLowerCase().includes(keyword)
      );
      if (!hasDish) return; // Bỏ qua bàn này nếu không có món đang tìm
    }

    // --- Phần render giữ nguyên như cũ ---
    let total = t.orders.reduce((sum, item) => sum + item.price * item.qty, 0);
    let statusText =
      t.status === "occupied"
        ? "Có khách"
        : t.status === "reserved"
        ? "Đặt trước"
        : "Trống";

    // Highlight viền đỏ nếu bàn này khớp kết quả tìm kiếm để dễ nhìn
    const highlightStyle =
      keyword !== ""
        ? "border: 2px solid #ef4444; transform: scale(1.05);"
        : "";

    grid.innerHTML += `
            <div class="table-card ${t.status}" onclick="openTableDetail(${
      t.id
    })" style="${highlightStyle}">
                <div class="table-icon"><i class="fas fa-chair"></i></div>
                <div class="table-name">${t.name}</div>
                <div class="table-info">${t.area}</div>
                <div class="table-info" style="font-weight:bold;margin-top:5px;">${statusText}</div>
                ${
                  t.status === "occupied"
                    ? `<div style="color:#ef4444; font-size:0.85rem; margin-top:5px;">${total.toLocaleString(
                        "vi-VN"
                      )}đ</div>`
                    : ""
                }
                ${
                  // Hiển thị thêm dòng nhỏ báo tìm thấy món (nếu đang tìm)
                  keyword !== ""
                    ? `<div style="font-size:0.75rem; color:#fff; background:#ef4444; border-radius:4px; margin-top:5px;">Đang có món này</div>`
                    : ""
                }
            </div>`;
  });

  // Thông báo nếu không tìm thấy
  if (grid.innerHTML === "") {
    grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; color: #64748b; padding: 20px;">Không tìm thấy bàn nào có món "${keyword}" tại ${
      currentTableArea === "all" ? "tất cả các tầng" : currentTableArea
    }</div>`;
  }
}

// --- CẬP NHẬT: Hàm filterTables để lưu trạng thái ---
function filterTables(area) {
  // 1. Cập nhật biến toàn cục
  currentTableArea = area;

  // 2. Xử lý UI active button
  document
    .querySelectorAll("#view-tables .filter-btn")
    .forEach((btn) => btn.classList.remove("active"));

  // Tìm button được click (dựa vào text content vì event.target có thể trượt)
  // Cách đơn giản nhất là dùng event.target như cũ, nhưng ta thêm logic check text
  const btns = document.querySelectorAll("#view-tables .filter-btn");
  btns.forEach((btn) => {
    if (area === "all" && btn.innerText === "Tất cả")
      btn.classList.add("active");
    else if (btn.innerText === area) btn.classList.add("active");
  });

  // 3. Gọi render lại
  renderTables();
}
function openTableDetail(id) {
  const t = tableData.find((x) => x.id === id);
  currentTableId = id;
  if (t) {
    document.getElementById("td-table-name").innerText = t.name;
    document.getElementById("td-table-area").innerText = `Khu vực: ${t.area}`;
    document.getElementById("td-status-select").value = t.status;
    document.getElementById("td-time-in").innerText = t.timeIn || "--:--";

    const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=Table-${t.id}`;
    document.getElementById("td-qr-img").src = qrUrl;

    renderTableOrders(t);
    renderTableHistory(t);
    switchTableTab("order");
    document.getElementById("tableDetailModal").style.display = "block";
  }
}

function renderTableOrders(table) {
  const list = document.getElementById("td-order-list");
  list.innerHTML = "";
  let subtotal = 0;

  table.orders.forEach((item, index) => {
    subtotal += item.price * item.qty;
    const statusSelect = `
            <select class="item-status-select status-${
              item.status
            }" onchange="updateItemStatus(${index}, this.value)">
                <option value="cooking" ${
                  item.status === "cooking" ? "selected" : ""
                }>Đang làm</option>
                <option value="ready" ${
                  item.status === "ready" ? "selected" : ""
                }>Sẵn sàng</option>
                <option value="served" ${
                  item.status === "served" ? "selected" : ""
                }>Đã phục vụ</option>
            </select>`;

    list.innerHTML += `
            <tr>
                <td style="font-weight:bold;">${item.name}</td>
                <td>${item.qty}</td>
                <td style="color:#666; font-size:0.85rem;">${
                  item.note || "-"
                }</td>
                <td>${statusSelect}</td>
                <td style="font-weight:bold;">${(
                  item.price * item.qty
                ).toLocaleString("vi-VN")}đ</td>
            </tr>`;
  });

  document.getElementById("td-subtotal").innerText =
    subtotal.toLocaleString("vi-VN") + "đ";
  document.getElementById("td-discount").innerText = "-0đ";
  document.getElementById("td-final-total").innerText =
    subtotal.toLocaleString("vi-VN") + "đ";
  document.getElementById("td-final-total").dataset.subtotal = subtotal;
}

function updateItemStatus(index, newStatus) {
  const t = tableData.find((x) => x.id === currentTableId);
  if (t) {
    t.orders[index].status = newStatus;
    if (newStatus === "ready")
      showAlert(
        "Món ăn sẵn sàng!",
        `Món <b>${t.orders[index].name}</b> tại ${t.name} đã nấu xong.`
      );
    renderTableOrders(t);
  }
}

// --- TRONG FILE script.js ---

/* ============================================================
   1. HÀM XỬ LÝ NÚT "THÊM MÃ" Ở MÀN HÌNH QUẢN LÝ (TÍNH NĂNG MỚI)
   (Dùng cho ô nhập liệu như trong ảnh Sếp gửi)
   ============================================================ */
function addPromotion() {
  // Lấy mã từ ô input ở màn hình quản lý (ID khác với trong modal)
  const code = document
    .getElementById("promo-code-input")
    .value.toUpperCase()
    .trim();
  let discountRate = 0;

  // Logic kiểm tra mã (Dùng chung logic Regex của Sếp)
  if (promotions[code]) {
    discountRate = promotions[code];
  } else {
    const regex = /^CHIEN([1-9]|[1-5][0-9]|60)$/;
    const match = code.match(regex);
    if (match) {
      discountRate = parseInt(match[1]) / 100;
    }
  }

  // Nếu mã hợp lệ -> Áp dụng cho TẤT CẢ bàn đang có khách
  if (discountRate > 0) {
    let count = 0;
    tableData.forEach((t) => {
      // Chỉ áp dụng bàn đang có khách (occupied) và đã gọi món
      if (t.status === "occupied" && t.orders.length > 0) {
        t.activeDiscountRate = discountRate; // Lưu % giảm vào dữ liệu bàn
        t.activeDiscountCode = code; // Lưu tên mã vào dữ liệu bàn
        count++;
      }
    });

    if (count > 0) {
      alert(
        `✅ Đã áp dụng mã ${code} (Giảm ${
          discountRate * 100
        }%) cho ${count} bàn đang phục vụ!`
      );
      renderTables(); // Vẽ lại sơ đồ bàn để cập nhật (nếu cần)
    } else {
      alert("⚠️ Mã hợp lệ nhưng hiện tại không có bàn nào đang phục vụ!");
    }
  } else {
    alert("❌ Mã giảm giá không hợp lệ hoặc sai định dạng!");
  }
}

/* ============================================================
   2. HÀM HIỂN THỊ CHI TIẾT ĐƠN HÀNG (CẬP NHẬT)
   (Cần hàm này để khi mở bàn lên, nó tự hiện mã giảm giá đã nhập ở ngoài)
   ============================================================ */
function renderTableOrders(table) {
  const list = document.getElementById("td-order-list");
  list.innerHTML = "";
  let subtotal = 0;

  // Render danh sách món ăn
  table.orders.forEach((item, index) => {
    subtotal += item.price * item.qty;
    // Tạo select chọn trạng thái món
    const statusSelect = `
            <select class="item-status-select status-${
              item.status
            }" onchange="updateItemStatus(${index}, this.value)">
                <option value="cooking" ${
                  item.status === "cooking" ? "selected" : ""
                }>Đang làm</option>
                <option value="ready" ${
                  item.status === "ready" ? "selected" : ""
                }>Sẵn sàng</option>
                <option value="served" ${
                  item.status === "served" ? "selected" : ""
                }>Đã phục vụ</option>
            </select>`;

    list.innerHTML += `
            <tr>
                <td style="font-weight:bold;">${item.name}</td>
                <td>${item.qty}</td>
                <td style="color:#666; font-size:0.85rem;">${
                  item.note || "-"
                }</td>
                <td>${statusSelect}</td>
                <td style="font-weight:bold;">${(
                  item.price * item.qty
                ).toLocaleString("vi-VN")}đ</td>
            </tr>`;
  });

  // --- LOGIC HIỂN THỊ GIẢM GIÁ (Kết nối với tính năng thêm mã toàn cục) ---
  let discountAmount = 0;

  // Nếu bàn này đã có mã giảm giá (từ hàm addPromotion hoặc applyPromotion lưu vào)
  if (table.activeDiscountRate && table.activeDiscountRate > 0) {
    discountAmount = subtotal * table.activeDiscountRate;
    // Điền sẵn mã vào ô input trong modal để Sếp thấy
    document.getElementById("td-promo-input").value =
      table.activeDiscountCode || "";
  } else {
    document.getElementById("td-promo-input").value = "";
  }

  const finalTotal = subtotal - discountAmount;

  // Cập nhật giao diện
  document.getElementById("td-subtotal").innerText =
    subtotal.toLocaleString("vi-VN") + "đ";
  document.getElementById(
    "td-discount"
  ).innerText = `-${discountAmount.toLocaleString("vi-VN")}đ`;
  document.getElementById("td-final-total").innerText =
    finalTotal.toLocaleString("vi-VN") + "đ";

  // Lưu tạm subtotal vào dataset để hàm applyPromotion của Sếp dùng tính toán
  document.getElementById("td-final-total").dataset.subtotal = subtotal;
}

/* ============================================================
   3. HÀM APPLY KHUYẾN MÃI (CODE CỦA SẾP)
   (Tôi giữ nguyên logic, chỉ thêm đoạn lưu dữ liệu vào tableData)
   ============================================================ */
function applyPromotion() {
  const inputCode = document
    .getElementById("td-promo-input")
    .value.toUpperCase()
    .trim();
  const subtotal = parseInt(
    document.getElementById("td-final-total").dataset.subtotal
  );

  let discountRate = 0; // Tỉ lệ giảm (VD: 0.1 là 10%)

  // 1. Kiểm tra trong danh sách Khuyến mãi cố định (nếu có)
  if (promotions[inputCode]) {
    discountRate = promotions[inputCode];
  }
  // 2. Kiểm tra mã động: CHIEN + [1-60]
  else {
    // Regex giải thích:
    // ^CHIEN      : Bắt đầu bằng chữ CHIEN
    // ( ... )     : Nhóm lấy số
    // [1-9]       : Số từ 1 đến 9 (VD: CHIEN5)
    // |           : Hoặc
    // [1-5][0-9]  : Số từ 10 đến 59 (VD: CHIEN15, CHIEN59)
    // |           : Hoặc
    // 60          : Số 60
    // $           : Kết thúc chuỗi
    const regex = /^CHIEN([1-9]|[1-5][0-9]|60)$/;
    const match = inputCode.match(regex);

    if (match) {
      // match[1] là con số lấy được (ví dụ '25' trong CHIEN25)
      discountRate = parseInt(match[1]) / 100;
    }
  }

  // 3. Tính toán và hiển thị
  if (discountRate > 0) {
    const discountAmount = subtotal * discountRate;
    const finalTotal = subtotal - discountAmount;

    document.getElementById(
      "td-discount"
    ).innerText = `-${discountAmount.toLocaleString("vi-VN")}đ`;
    document.getElementById("td-final-total").innerText =
      finalTotal.toLocaleString("vi-VN") + "đ";

    // --- [ĐOẠN MỚI THÊM VÀO] ---
    // Lưu trạng thái vào dữ liệu gốc để khi đóng modal không bị mất
    const t = tableData.find((x) => x.id === currentTableId);
    if (t) {
      t.activeDiscountRate = discountRate;
      t.activeDiscountCode = inputCode;
    }
    // ---------------------------

    // Hiển thị phần trăm giảm để dễ check
    const percent = discountRate * 100;
    showAlert("Thành công!", `Đã áp dụng mã ${inputCode} (Giảm ${percent}%)`);
  } else {
    alert("Mã giảm giá không hợp lệ hoặc vượt quá giới hạn (1-60%)!");

    // --- [ĐOẠN MỚI THÊM VÀO] ---
    // Nếu mã sai thì reset lại dữ liệu gốc của bàn
    const t = tableData.find((x) => x.id === currentTableId);
    if (t) {
      t.activeDiscountRate = 0;
      t.activeDiscountCode = "";
    }
    // ---------------------------

    // Reset lại nếu mã sai
    document.getElementById("td-discount").innerText = "-0đ";
    document.getElementById("td-final-total").innerText =
      subtotal.toLocaleString("vi-VN") + "đ";
  }
}
function changeTableStatusFromSelect(status) {
  const t = tableData.find((x) => x.id === currentTableId);
  if (t) {
    t.status = status;
    if (status === "occupied" && !t.timeIn) {
      const now = new Date();
      t.timeIn =
        now.getHours() + ":" + String(now.getMinutes()).padStart(2, "0");
      document.getElementById("td-time-in").innerText = t.timeIn;
    }
    renderTables();
  }
}

function checkoutTable() {
  const t = tableData.find((x) => x.id === currentTableId);
  if (t && t.orders.length > 0) {
    if (confirm("Xác nhận thanh toán và trả bàn?")) {
      const totalStr = document.getElementById("td-final-total").innerText;
      t.history.unshift({
        time: `${t.timeIn} - Now`,
        info: `Thanh toán: ${totalStr} (${t.orders.length} món)`,
      });
      t.orders = [];
      t.status = "empty";
      t.timeIn = null;
      renderTables();
      closeModal("tableDetailModal");
      showAlert(
        "Thanh toán thành công!",
        `Bàn ${t.name} đã thanh toán ${totalStr}.`
      );
    }
  } else {
    alert("Bàn trống hoặc chưa có món!");
  }
}

function printTableQR() {
  const table = tableData.find((t) => t.id === currentTableId);
  if (!table) return;
  const qrSrc = document.getElementById("td-qr-img").src;
  const printWindow = window.open("", "", "height=600,width=500");
  printWindow.document.write(
    `<html><head><title>In QR</title><style>body{display:flex;justify-content:center;align-items:center;height:100vh;margin:0;}.card{text-align:center;border:2px dashed #333;padding:20px;width:300px;}</style></head><body><div class="card"><h1>${table.name}</h1><img src="${qrSrc}" width="200"><p>Quét để gọi món</p></div></body></html>`
  );
  printWindow.document.close();
  printWindow.focus();
  setTimeout(() => {
    printWindow.print();
    printWindow.close();
  }, 500);
}

function switchTableTab(tabName) {
  document.getElementById("tab-table-order").style.display =
    tabName === "order" ? "flex" : "none";
  document.getElementById("tab-table-history").style.display =
    tabName === "history" ? "block" : "none";
}

function renderTableHistory(table) {
  const list = document.getElementById("td-history-list");
  list.innerHTML =
    table.history.length === 0
      ? '<li style="text-align:center; color:#999; padding:10px;">Chưa có lịch sử</li>'
      : table.history
          .map(
            (h) =>
              `<li class="history-item"><span class="history-info">${h.info}</span><span class="history-time">${h.time}</span></li>`
          )
          .join("");
}

// --- 5. QUẢN LÝ ĐƠN HÀNG ---
function renderOrders(filter = "all") {
  const container = document.getElementById("order-list-container");
  container.innerHTML = "";
  ordersData.forEach((order) => {
    if (filter !== "all" && order.status !== filter) return;
    const statusBadge =
      order.status === "pending"
        ? '<span class="badge badge-pending">Chờ bếp</span>'
        : '<span class="badge badge-completed">Hoàn thành</span>';
    container.innerHTML += `<tr onclick="openOrderDetail(${order.id})"><td>#${order.id}</td><td style="font-weight:bold;">${order.table}</td><td>${order.time}</td><td style="color:var(--status-red); font-weight:bold;">${order.total}</td><td>${statusBadge}</td><td><button class="status-btn">Chi tiết</button></td></tr>`;
  });
}
function filterOrders(status) {
  document
    .querySelectorAll("#view-orders .filter-btn")
    .forEach((btn) => btn.classList.remove("active"));
  event.target.classList.add("active");
  renderOrders(status);
}
function openOrderDetail(id) {
  const order = ordersData.find((o) => o.id === id);
  if (order) {
    currentOrderId = id;
    document.getElementById("order-id-modal").innerText = "#" + order.id;
    document.getElementById("order-total-modal").innerText = order.total;
    document.getElementById("order-items-list").innerHTML = order.items
      .map(
        (item) =>
          `<div style="display:flex; justify-content:space-between; margin-bottom:5px;"><span><b>${item.qty}x</b> ${item.name}</span><span>${item.price}</span></div>`
      )
      .join("");
    document.getElementById("orderModal").style.display = "block";
  }
}
function completeOrder() {
  const order = ordersData.find((o) => o.id === currentOrderId);
  if (order) {
    order.status = "completed";
    renderOrders();
    closeModal("orderModal");
    addNotification(`Đơn #${order.id} hoàn thành`, "status");
  }
}

// --- 6. QUẢN LÝ NHÂN VIÊN ---
function renderStaff(data = staffData) {
  const container = document.getElementById("staff-grid-container");
  container.innerHTML = "";
  data.forEach((staff) => {
    if (!staff.salary) {
      staff.info = { phone: "--", dob: "--", address: "--" };
      staff.schedule = "--";
      staff.salary = { basic: "0", bonus: "0", total: "0" };
    }
    const statusClass =
      staff.status === "online" ? "dot-online" : "dot-offline";
    const card = `
            <div class="staff-card" id="staff-card-${staff.id}" onclick="toggleStaffExpand(${staff.id})">
                <img src="${staff.img}" class="staff-avatar">
                <div class="staff-info"><div class="staff-name">${staff.name}</div><div class="staff-role">${staff.role}</div><div style="font-size:0.8rem; margin-top:8px;"><span class="staff-status-dot ${statusClass}"></span> ${staff.status}</div></div>
                <div class="expand-icon"><i class="fas fa-chevron-down"></i></div>
                <div class="staff-details-expand" id="staff-details-${staff.id}">
                    <div class="detail-section"><div class="detail-title"><i class="fas fa-id-card"></i> Thông tin</div><div class="detail-content">SĐT: ${staff.info.phone}<br>ĐC: ${staff.info.address}</div></div>
                    <div class="detail-section"><div class="detail-title"><i class="fas fa-calendar-alt"></i> Lịch</div><div class="detail-content">${staff.schedule}</div></div>
                    <div class="detail-section"><div class="detail-title"><i class="fas fa-money-bill-wave"></i> Lương</div><div class="detail-content">Tổng: ${staff.salary.total}đ</div></div>
                </div>
                <div class="staff-actions"><button class="icon-btn btn-edit" onclick="event.stopPropagation(); openEditStaff(${staff.id})"><i class="fas fa-pen"></i></button><button class="icon-btn btn-delete" onclick="event.stopPropagation(); deleteStaff(${staff.id})"><i class="fas fa-trash"></i></button></div>
            </div>`;
    container.innerHTML += card;
  });
}
function toggleStaffExpand(id) {
  document.getElementById(`staff-card-${id}`).classList.toggle("expanded");
}
function searchStaff() {
  const k = document.getElementById("staff-search-input").value.toLowerCase();
  renderStaff(staffData.filter((s) => s.name.toLowerCase().includes(k)));
}
function openStaffModal() {
  isEditingStaff = false;
  resetStaffForm();
  document.getElementById("staffModal").style.display = "block";
}
function openEditStaff(id) {
  const s = staffData.find((x) => x.id === id);
  if (s) {
    isEditingStaff = true;
    currentStaffId = id;
    document.getElementById("staff-modal-title").innerText = "Cập nhật";
    document.getElementById("staff-name-input").value = s.name;
    document.getElementById("staff-role-input").value = s.role;
    document.getElementById("staff-status-input").value = s.status;
    document.getElementById("staff-img-input").value = s.img;
    document.getElementById("staff-preview-img").src = s.img;
    document.getElementById("staff-phone").value = s.info.phone;
    document.getElementById("staff-dob").value = s.info.dob;
    document.getElementById("staff-address").value = s.info.address;
    document.getElementById("staff-schedule").value = s.schedule;
    document.getElementById("staff-salary-basic").value = s.salary.basic;
    document.getElementById("staff-salary-bonus").value = s.salary.bonus;
    document.getElementById("staffModal").style.display = "block";
  }
}
function saveStaff() {
  const name = document.getElementById("staff-name-input").value;
  if (!name) return alert("Nhập tên!");
  const role = document.getElementById("staff-role-input").value;
  const status = document.getElementById("staff-status-input").value;
  const img =
    document.getElementById("staff-img-input").value ||
    "https://via.placeholder.com/100";
  const info = {
    phone: document.getElementById("staff-phone").value,
    dob: document.getElementById("staff-dob").value,
    address: document.getElementById("staff-address").value,
  };
  const schedule = document.getElementById("staff-schedule").value;
  const basic = document.getElementById("staff-salary-basic").value || "0";
  const bonus = document.getElementById("staff-salary-bonus").value || "0";
  const total = (
    parseInt(basic.replace(/\./g, "")) + parseInt(bonus.replace(/\./g, ""))
  ).toLocaleString("vi-VN");
  const staffObj = {
    id: isEditingStaff ? currentStaffId : Date.now(),
    name,
    role,
    status,
    img,
    info,
    schedule,
    salary: { basic, bonus, total },
  };

  if (isEditingStaff) {
    const idx = staffData.findIndex((s) => s.id === currentStaffId);
    if (idx !== -1) staffData[idx] = staffObj;
    addNotification(`Cập nhật NV: ${name}`, "info");
  } else {
    staffData.push(staffObj);
    addNotification(`Thêm NV: ${name}`, "add");
  }
  renderStaff();
  closeModal("staffModal");
}
function deleteStaff(id) {
  if (confirm("Xóa?")) {
    staffData = staffData.filter((s) => s.id !== id);
    renderStaff();
    addNotification("Đã xóa NV", "delete");
  }
}
function resetStaffForm() {
  document.querySelectorAll("#staffModal input").forEach((i) => (i.value = ""));
  document.getElementById("staff-preview-img").src =
    "https://via.placeholder.com/100";
}

// --- HỆ THỐNG THÔNG BÁO ---
function addNotification(msg, type = "info") {
  notifications.unshift({
    id: Date.now(),
    message: msg,
    time: new Date().toLocaleTimeString(),
    icon: "📝",
    isRead: false,
  });
  renderNotifications();
}
function renderNotifications() {
  const b = document.getElementById("noti-badge");
  const c = notifications.filter((n) => !n.isRead).length;
  b.style.display = c > 0 ? "inline-block" : "none";
  b.innerText = c;
  document.getElementById("noti-list").innerHTML = notifications
    .map(
      (n) =>
        `<div class="noti-item ${
          n.isRead ? "" : "unread"
        }" onclick="markAsRead(${n.id})"><div class="noti-icon">${
          n.icon
        }</div><div class="noti-content"><div class="noti-title">${
          n.message
        }</div><div class="noti-time">${n.time}</div></div></div>`
    )
    .join("");
}
function markAsRead(id) {
  const n = notifications.find((x) => x.id === id);
  if (n) {
    n.isRead = true;
    renderNotifications();
  }
}
function toggleNotiDropdown() {
  const d = document.getElementById("noti-dropdown");
  d.style.display = d.style.display === "block" ? "none" : "block";
}
function showAlert(title, msg) {
  document.getElementById("alert-title").innerText = title;
  document.getElementById("alert-msg").innerHTML = msg;
  document.getElementById("alert-toast").classList.add("show");
  setTimeout(
    () => document.getElementById("alert-toast").classList.remove("show"),
    5000
  );
}
function closeAlert() {
  document.getElementById("alert-toast").classList.remove("show");
}

// COMMON
function closeModal(id) {
  document.getElementById(id).style.display = "none";
}
window.onclick = function (e) {
  if (e.target.classList.contains("modal")) e.target.style.display = "none";
  if (!e.target.closest(".noti-wrapper"))
    document.getElementById("noti-dropdown").style.display = "none";
};

// CHART & INIT
function drawDonutChart(containerId, data, centerText) {
  const container = document.getElementById(containerId);
  if (!container) return;
  const size = 180,
    cx = 90,
    cy = 90,
    radius = 55;
  let currentAngle = 0;
  let svgHtml = `<svg width="100%" height="100%" viewBox="0 0 ${size} ${size}" style="overflow: visible;">`;
  data.forEach((item) => {
    const sliceAngle = (item.value / 100) * 2 * Math.PI;
    const x1 = cx + radius * Math.cos(currentAngle),
      y1 = cy + radius * Math.sin(currentAngle);
    const x2 = cx + radius * Math.cos(currentAngle + sliceAngle),
      y2 = cy + radius * Math.sin(currentAngle + sliceAngle);
    const largeArcFlag = sliceAngle > Math.PI ? 1 : 0;
    const pathData = `M ${cx} ${cy} L ${x1} ${y1} A ${radius} ${radius} 0 ${largeArcFlag} 1 ${x2} ${y2} Z`;
    svgHtml += `<path d="${pathData}" fill="${item.color}" class="chart-segment" onmousemove="showTooltip(evt, '${item.label}: ${item.info}')" onmouseleave="hideTooltip()"></path>`;
    currentAngle += sliceAngle;
  });
  svgHtml += `<circle cx="${cx}" cy="${cy}" r="${
    radius * 0.6
  }" fill="white" /></svg><div class="center-label">${centerText}</div>`;
  container.innerHTML = svgHtml;
}

window.onload = function () {
  renderMenu();
  renderTables();
  renderOrders();
  renderStaff();
  drawDonutChart("chart-revenue", chartData.revenue, "15.8tr");
  drawDonutChart("chart-table", chartData.table, "24 Bàn");
  drawDonutChart("chart-order", chartData.order, "75 Đơn");
};
// --- CODE MỚI: Xử lý mã giảm giá Menu ---
let currentMenuDiscount = 0; // Biến lưu % giảm giá hiện tại

function applyMenuDiscount() {
  const input = document
    .getElementById("menu-discount-input")
    .value.toUpperCase()
    .trim();

  // Regex kiểm tra: Bắt đầu bằng CHIEN, theo sau là số từ 1-9, hoặc 10-69, hoặc 70
  // Giải thích Regex:
  // ^CHIEN : Bắt đầu bằng chữ CHIEN
  // (?: ... ) : Nhóm không lưu
  // [1-9]    : Số từ 1 đến 9
  // |        : Hoặc
  // [1-6][0-9] : Số từ 10 đến 69
  // |        : Hoặc
  // 70       : Số 70
  // $        : Kết thúc chuỗi
  const regex = /^CHIEN(?:[1-9]|[1-6][0-9]|70)$/;

  if (regex.test(input)) {
    // Lấy phần số ra khỏi chuỗi (VD: CHIEN20 -> lấy 20)
    currentMenuDiscount = parseInt(input.replace("CHIEN", ""));

    // Hiệu ứng visual cho ô input khi đúng
    document.getElementById("menu-discount-input").style.borderColor =
      "#10b981"; // Xanh
  } else {
    currentMenuDiscount = 0;

    // Hiệu ứng visual khi sai hoặc trống
    if (input.length > 0) {
      document.getElementById("menu-discount-input").style.borderColor =
        "#ef4444"; // Đỏ
    } else {
      document.getElementById("menu-discount-input").style.borderColor =
        "#cbd5e1"; // Xám
    }
  }

  // Vẽ lại menu với giá mới
  renderMenu();
}
// =========================================
// CHATBOT AI LOGIC (QUẢN LÝ THÔNG MINH)
// =========================================

// Chat client (frontend) - updated to call backend AI proxy
// Lưu lịch sử hội thoại (gửi một phần lịch sử nếu bạn muốn)
let chatHistory = [
  {
    role: "user",
    parts: [
      {
        text: "Bạn là Trợ lý ảo quản lý nhà hàng. Trả lời ngắn gọn, vui vẻ, gọi người dùng là 'Sếp'.",
      },
    ],
  },
];

// --- UI helpers ---
function toggleChatbot() {
  const chat = document.getElementById("chatbot-widget");

  // KIỂM TRA AN TOÀN: Nếu không tìm thấy khung chat thì dừng lại và báo lỗi ngầm
  if (!chat) {
    console.error(
      "Lỗi: Không tìm thấy phần tử HTML có id='chatbot-widget'. Hãy kiểm tra lại file HTML."
    );
    return;
  }

  chat.classList.toggle("active");

  // Focus vào ô nhập khi mở (thêm kiểm tra tồn tại cho ô input luôn)
  if (chat.classList.contains("active")) {
    setTimeout(() => {
      const input = document.getElementById("chat-input");
      if (input) input.focus();
    }, 300);
  }
}

function handleChatKey(e) {
  if (e.key === "Enter") sendChatMessage();
}

function addMessage(text, sender) {
  const box = document.getElementById("chat-messages");
  const div = document.createElement("div");
  div.className = `message ${sender}-msg`;
  div.innerHTML = text; // Cho phép HTML để format đẹp (cẩn thận nếu có input không tin cậy)
  box.appendChild(div);
  box.scrollTop = box.scrollHeight; // Cuộn xuống dưới
}
// Hàm thêm nút gợi ý (Quick Reply)
function addQuickReply(text) {
  const box = document.getElementById("chat-messages");
  const btn = document.createElement("div");

  btn.className = "quick-reply-btn"; // Class CSS mới tạo ở trên
  btn.innerText = text;

  // Khi bấm vào thì gửi tin nhắn đó đi
  btn.onclick = function () {
    document.getElementById("chat-input").value = text;
    sendChatMessage();
    // Tùy chọn: Xóa nút này đi sau khi bấm để đỡ rối
    // btn.remove();
  };

  // Animation xuất hiện
  btn.style.animation = "popIn 0.3s ease forwards";

  box.appendChild(btn);
  box.scrollTop = box.scrollHeight;
}

// Ví dụ cách dùng trong code init ban đầu:
/*
addMessage("Chào Sếp Trung! Em có thể giúp gì ạ?", "bot");
setTimeout(() => {
    addQuickReply("Báo cáo doanh thu hôm nay");
    addQuickReply("Tình trạng các bàn hiện tại");
}, 500);
*/
function showTyping() {
  const box = document.getElementById("chat-messages");
  // Nếu indicator đã tồn tại thì không tạo thêm
  if (document.getElementById("typing-indicator")) return;
  const div = document.createElement("div");
  div.id = "typing-indicator";
  div.className = "message bot-msg";
  div.innerHTML = '<i class="fas fa-ellipsis-h fa-beat"></i> Đang suy nghĩ...';
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}

function removeTyping() {
  const el = document.getElementById("typing-indicator");
  if (el) el.remove();
}

// --- Local quick-intents (xử lý nhanh, không gọi AI) ---
function checkLocalResponse(text) {
  if (!text) return null;
  const t = text.toLowerCase().trim();

  // chào hỏi cơ bản
  const greetings = ["hi", "hello", "chào", "alo", "ê", "hey"];
  if (greetings.includes(t)) {
    return "Chào Sếp! 👋 Hôm nay Sếp muốn kiểm tra doanh thu hay soi tình trạng bàn nào ạ?";
  }

  if (t === "help" || t === "trợ giúp" || t === "hdsd") {
    return `🤖 <b>Em có thể giúp Sếp:</b><br>
            - "Doanh thu hôm nay bao nhiêu?"<br>
            - "Bàn 2 đang gọi món gì?"<br>
            - "Món nào bán chạy nhất?"<br>
            - "Viết status quảng cáo..."`;
  }

  if (t === "clear" || t === "xóa" || t === "reset") {
    chatHistory = [];
    return "🧹 Đã dọn dẹp bộ nhớ đệm. Em đã quên hết chuyện cũ rồi ạ!";
  }

  // Không có câu trả lời cục bộ
  return null;
}

// --- Call backend AI proxy ---
async function callGeminiAI(userMsg) {
  // Tập hợp dữ liệu nếu cần (cập nhật để gửi các dữ liệu thực tế của bạn)
  const websiteData = {
    thoi_gian: new Date().toLocaleString("vi-VN"),
    thuc_don: menuData, // Đã bỏ dấu //
    ban_an: tableData, // Đã bỏ dấu //
    doanh_thu_chart: chartData, // Đã bỏ dấu //
    don_hang: ordersData, // Đã bỏ dấu //
  };

  const finalPrompt = `
    DỮ LIỆU HỆ THỐNG (JSON): ${JSON.stringify(websiteData)}
    USER HỎI: "${userMsg}"
    YÊU CẦU:
    - Phân tích JSON để trả lời.
    - Nếu hỏi doanh thu tổng: cộng các nguồn thu trong 'doanh_thu_chart' và tiền đang phục vụ tại bàn (ban_an status 'occupied').
    - Trả lời ngắn gọn, vui vẻ, dùng icon. Định dạng HTML đơn giản (<b>, <br>).
  `;

  const requestBody = {
    contents: [
      ...chatHistory,
      { role: "user", parts: [{ text: finalPrompt }] },
    ],
  };

  // Lấy token do server inject vào trang (không phải API key)
  const APP_TOKEN = window.APP_TOKEN || "";

  if (!APP_TOKEN) {
    throw new Error(
      "Không có token frontend (APP_TOKEN). Vui lòng kiểm tra server render."
    );
  }

  const resp = await fetch("/api/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-APP-TOKEN": APP_TOKEN,
    },
    body: JSON.stringify({ model: "gemini-2.5-flash", requestBody }),
  });

  if (!resp.ok) {
    // Cố gắng parse JSON lỗi, fallback sang text
    let err;
    try {
      err = await resp.json();
    } catch (e) {
      err = { message: await resp.text() };
    }
    // Ném error cho gọi caller xử lý
    throw new Error(
      err.error?.detail || err.error || err.message || JSON.stringify(err)
    );
  }

  const data = await resp.json();

  // Defensive: kiểm tra cấu trúc trả về
  const textReply = data?.candidates?.[0]?.content?.parts?.[0]?.text;
  if (!textReply) {
    // Nếu model trả khác định dạng, thử lấy message gốc
    return data?.message || "Em xin lỗi, hiện tại không có phản hồi từ AI.";
  }

  return textReply;
}

// --- Gửi tin nhắn chính (điều phối local -> AI) ---
async function sendChatMessage() {
  const inputEl = document.getElementById("chat-input");
  const msg = inputEl.value.trim();
  if (!msg) return;

  // Hiện tin nhắn người dùng
  addMessage(msg, "user");
  inputEl.value = "";

  // Kiểm tra trả lời cục bộ trước
  const localReply = checkLocalResponse(msg);
  if (localReply) {
    // Hiện nhanh để user cảm thấy snappy
    setTimeout(() => addMessage(localReply, "bot"), 250);
    return;
  }

  // Nếu không, gọi backend AI
  showTyping();
  try {
    const botReply = await callGeminiAI(msg);
    removeTyping();
    addMessage(botReply, "bot");
  } catch (err) {
    removeTyping();
    const safeMsg =
      typeof err === "string"
        ? err
        : err.message || "Không thể kết nối tới dịch vụ AI.";
    console.error("AI call error:", err);
    addMessage(`⚠️ Lỗi: ${safeMsg}`, "bot");
  }
}
