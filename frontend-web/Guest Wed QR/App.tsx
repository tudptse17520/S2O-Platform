import React, { useState, useEffect, useMemo } from "react";
import {
  ShoppingBag,
  UtensilsCrossed,
  Clock,
  ChevronRight,
  Minus,
  Plus,
  Sparkles,
  ArrowLeft,
  Search,
  CheckCircle2,
  ChefHat,
  Receipt,
} from "lucide-react";
import { MOCK_MENU, CATEGORIES } from "./services/mockData";
import {
  MenuItem,
  CartItem,
  Order,
  SessionContext,
  OrderStatus,
} from "./types";
import { MenuCard } from "./components/MenuCard";
import { AIChat } from "./components/AIChat";
import { ItemDetailModal } from "./components/ItemDetailModal";
import { SplashScreen } from "./components/SplashScreen";

function App() {
  // --- State ---
  const [session, setSession] = useState<SessionContext | null>(null);
  const [view, setView] = useState<"menu" | "cart" | "status">("menu");
  const [activeCategory, setActiveCategory] = useState("Tất cả");
  const [searchQuery, setSearchQuery] = useState("");
  const [cart, setCart] = useState<CartItem[]>([]);
  const [orders, setOrders] = useState<Order[]>([]);
  const [isAIChating, setIsAIChating] = useState(false);

  // Loading & Splash State
  const [isLoadingData, setIsLoadingData] = useState(true);
  const [showSplash, setShowSplash] = useState(true);

  // Detail Modal State
  const [selectedItem, setSelectedItem] = useState<MenuItem | null>(null);
  const [isDetailOpen, setIsDetailOpen] = useState(false);

  // --- Effects ---

  // 1. Initialize Session
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    // Simulate data fetching
    setTimeout(() => {
      setSession({
        tenantId: params.get("tenant") || "A1211",
        branchId: params.get("branch") || "Binh Thanh",
        tableId: params.get("table") || "36",
        token: params.get("token") || "valid-jwt-token",
      });
      setIsLoadingData(false);
    }, 1500); // Data loads slightly faster than splash animation to ensure smoothness
  }, []);

  // 2. Simulate Realtime Order Updates
  useEffect(() => {
    if (orders.length === 0) return;
    const interval = setInterval(() => {
      setOrders((prevOrders) => {
        return prevOrders.map((order) => {
          if (order.status === "pending")
            return { ...order, status: "preparing" };
          if (order.status === "preparing" && Math.random() > 0.7)
            return { ...order, status: "ready" };
          if (order.status === "ready" && Math.random() > 0.7)
            return { ...order, status: "served" };
          return order;
        });
      });
    }, 5000);
    return () => clearInterval(interval);
  }, [orders]);

  // --- Handlers ---

  const handleOpenDetail = (item: MenuItem) => {
    setSelectedItem(item);
    setIsDetailOpen(true);
  };

  const handleQuickAdd = (item: MenuItem, e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent opening modal
    handleAddToCart(item, 1, "");
  };

  const handleAddToCart = (item: MenuItem, quantity: number, notes: string) => {
    setCart((prev) => {
      // Find item with exact same ID and Notes (simple variant check)
      const existingIndex = prev.findIndex(
        (i) => i.id === item.id && i.notes === notes,
      );

      if (existingIndex > -1) {
        const newCart = [...prev];
        newCart[existingIndex].quantity += quantity;
        return newCart;
      }
      return [...prev, { ...item, quantity, notes }];
    });
  };

  const handleUpdateQuantity = (itemIndex: number, delta: number) => {
    setCart((prev) => {
      return prev
        .map((item, idx) => {
          if (idx === itemIndex) {
            return { ...item, quantity: Math.max(0, item.quantity + delta) };
          }
          return item;
        })
        .filter((item) => item.quantity > 0);
    });
  };

  const handlePlaceOrder = async () => {
    if (!cart.length || !session) return;
    setIsLoadingData(true);
    await new Promise((resolve) => setTimeout(resolve, 1500)); // Simulate longer network delay

    const newOrder: Order = {
      id: `ORD-${Date.now()}`,
      tableId: session.tableId,
      items: [...cart],
      status: "pending",
      totalAmount: cart.reduce(
        (sum, item) => sum + item.price * item.quantity,
        0,
      ),
      createdAt: new Date().toISOString(),
    };

    setOrders((prev) => [newOrder, ...prev]);
    setCart([]);
    setView("status");
    setIsLoadingData(false);
  };

  // --- Derived State ---
  const filteredMenu = useMemo(() => {
    let items = MOCK_MENU;

    // Filter by Category
    if (activeCategory !== "Tất cả") {
      items = items.filter((item) => item.category === activeCategory);
    }

    // Filter by Search
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      items = items.filter(
        (item) =>
          item.name.toLowerCase().includes(query) ||
          item.description.toLowerCase().includes(query),
      );
    }

    return items;
  }, [activeCategory, searchQuery]);

  const cartTotal = cart.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0,
  );
  const totalItemsInCart = cart.reduce((sum, item) => sum + item.quantity, 0);

  // --- UI Helpers ---

  const TimelineItem = ({
    active,
    completed,
    label,
    icon: Icon,
    isLast,
  }: any) => (
    <div className="flex flex-col items-center flex-1 relative z-10">
      <div
        className={`w-8 h-8 rounded-full flex items-center justify-center mb-2 transition-all duration-500 border ${
          completed || active
            ? "bg-orange-600 text-white border-orange-500 shadow-[0_0_10px_rgba(234,88,12,0.5)] scale-110"
            : "bg-slate-800 border-slate-700 text-slate-500"
        }`}
      >
        <Icon size={14} />
      </div>
      <span
        className={`text-[10px] font-medium text-center ${active || completed ? "text-orange-500" : "text-slate-500"}`}
      >
        {label}
      </span>
      {!isLast && (
        <div
          className={`absolute top-4 left-[50%] w-full h-0.5 -z-10 ${completed ? "bg-orange-600" : "bg-slate-800"}`}
        />
      )}
    </div>
  );

  // --- Main Render ---
  return (
    <div className="min-h-screen bg-slate-950 font-sans text-slate-100 pb-24">
      {/* Splash Screen Overlay */}
      {showSplash && <SplashScreen onFinish={() => setShowSplash(false)} />}

      {/* Only show main content when data is ready (splash handles the visual loading) */}
      {!isLoadingData && (
        <>
          {/* --- HEADER --- */}
          <header
            className={`sticky top-0 z-30 transition-all duration-300 ${view === "menu" ? "bg-slate-950/90 backdrop-blur-md shadow-lg shadow-black/20" : "bg-slate-950/80 backdrop-blur-md border-b border-slate-800"}`}
          >
            <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3">
              <div className="flex justify-between items-center mb-3">
                <div>
                  <h1 className="text-xl font-bold text-white flex items-center gap-2">
                    <div className="bg-orange-600 p-1.5 rounded-lg text-white shadow-lg shadow-orange-900/50">
                      <UtensilsCrossed size={18} />
                    </div>
                    ANH HAI
                  </h1>
                  <div className="text-xs text-slate-400 mt-1 flex gap-2">
                    <span className="bg-slate-800 px-2 py-0.5 rounded text-slate-300 border border-slate-700">
                      Bàn {session?.tableId}
                    </span>
                    <span>•</span>
                    <span>CN {session?.branchId}</span>
                  </div>
                </div>

                <button
                  onClick={() => setView("status")}
                  className="relative p-2.5 bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-orange-500 rounded-xl transition-all border border-slate-700"
                >
                  <Clock size={24} />
                  {orders.length > 0 && (
                    <span className="absolute top-2 right-2 w-2.5 h-2.5 bg-red-500 border-2 border-slate-800 rounded-full animate-pulse" />
                  )}
                </button>
              </div>

              {/* Search Bar (Only in Menu) */}
              {view === "menu" && (
                <div className="relative mb-2">
                  <Search
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"
                    size={18}
                  />
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Tìm món ăn..."
                    className="w-full bg-slate-900 border border-slate-800 rounded-2xl py-2.5 pl-10 pr-4 text-sm text-white focus:ring-2 focus:ring-orange-600 focus:border-transparent transition-all outline-none placeholder:text-slate-600"
                  />
                </div>
              )}
            </div>

            {/* Categories (Sticky below header) */}
            {view === "menu" && (
              <div className="max-w-7xl mx-auto px-4 sm:px-6 pb-3 overflow-x-auto no-scrollbar flex gap-2 snap-x">
                {CATEGORIES.map((cat) => (
                  <button
                    key={cat}
                    onClick={() => setActiveCategory(cat)}
                    className={`whitespace-nowrap px-4 py-2 rounded-full text-sm font-semibold transition-all snap-start ${
                      activeCategory === cat
                        ? "bg-orange-600 text-white shadow-lg shadow-orange-900/50 transform scale-105"
                        : "bg-slate-900 border border-slate-800 text-slate-400 hover:bg-slate-800 hover:text-white"
                    }`}
                  >
                    {cat}
                  </button>
                ))}
              </div>
            )}
          </header>

          {/* --- MAIN CONTENT --- */}
          <main className="max-w-7xl mx-auto p-4 sm:p-6 min-h-[calc(100vh-180px)]">
            {/* VIEW: MENU */}
            {view === "menu" && (
              <div className="animate-in fade-in duration-500">
                {filteredMenu.length === 0 ? (
                  <div className="text-center py-12">
                    <div className="bg-slate-900 w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-4 border border-slate-800">
                      <Search size={32} className="text-slate-600" />
                    </div>
                    <h3 className="text-lg font-medium text-white">
                      Không tìm thấy món
                    </h3>
                    <p className="text-slate-500 text-sm mt-1">
                      Thử tìm từ khóa khác xem sao nhé!
                    </p>
                  </div>
                ) : (
                  <>
                    <div className="flex justify-between items-center mb-4">
                      <h2 className="font-bold text-white text-lg border-l-4 border-orange-600 pl-3">
                        {activeCategory}
                      </h2>
                      <span className="text-xs text-slate-400 bg-slate-800 px-2 py-1 rounded-full border border-slate-700">
                        {filteredMenu.length} món
                      </span>
                    </div>
                    {/* Responsive Grid */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-6">
                      {filteredMenu.map((item) => (
                        <MenuCard
                          key={item.id}
                          item={item}
                          onPress={handleOpenDetail}
                          onQuickAdd={handleQuickAdd}
                        />
                      ))}
                    </div>
                  </>
                )}
              </div>
            )}

            {/* VIEW: CART */}
            {view === "cart" && (
              <div className="animate-in slide-in-from-right duration-300 max-w-3xl mx-auto">
                <div className="flex items-center gap-2 mb-6">
                  <button
                    onClick={() => setView("menu")}
                    className="p-2 -ml-2 hover:bg-slate-800 rounded-full text-slate-400 hover:text-white transition-colors"
                  >
                    <ArrowLeft size={24} />
                  </button>
                  <h2 className="text-2xl font-bold text-white">Giỏ hàng</h2>
                </div>

                {cart.length === 0 ? (
                  <div className="text-center py-16 flex flex-col items-center">
                    <div className="bg-slate-900 p-6 rounded-full mb-4 border border-slate-800">
                      <ShoppingBag size={48} className="text-slate-700" />
                    </div>
                    <h3 className="text-lg font-semibold text-white mb-2">
                      Giỏ hàng trống
                    </h3>
                    <p className="text-slate-500 mb-6 max-w-[200px]">
                      Hãy chọn vài món ngon từ thực đơn để thưởng thức nhé!
                    </p>
                    <button
                      onClick={() => setView("menu")}
                      className="bg-orange-600 text-white px-8 py-3 rounded-2xl font-bold hover:bg-orange-700 transition-colors shadow-lg shadow-orange-900/30"
                    >
                      Xem thực đơn
                    </button>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {cart.map((item, idx) => (
                      <div
                        key={`${item.id}-${idx}`}
                        className="bg-slate-900 p-4 rounded-3xl shadow-sm border-t-2 border-t-orange-200/60 border-b-2 border-b-white/10 border-x border-x-slate-800 flex gap-4"
                      >
                        <img
                          src={item.image}
                          alt={item.name}
                          className="w-20 h-20 object-cover rounded-2xl bg-slate-800"
                        />
                        <div className="flex-1 flex flex-col justify-between min-w-0">
                          <div>
                            <div className="flex justify-between items-start">
                              <h4 className="font-bold text-white truncate pr-2">
                                {item.name}
                              </h4>
                              <button
                                onClick={() =>
                                  handleUpdateQuantity(idx, -item.quantity)
                                }
                                className="text-slate-500 hover:text-red-500 transition-colors"
                              >
                                <Minus size={14} />
                              </button>
                            </div>
                            <p className="text-orange-500 font-bold text-sm">
                              {new Intl.NumberFormat("vi-VN").format(
                                item.price,
                              )}
                              đ
                            </p>
                            {item.notes && (
                              <p className="text-xs text-slate-400 bg-slate-800 p-1.5 rounded mt-1 truncate border border-slate-700">
                                Ghi chú: {item.notes}
                              </p>
                            )}
                          </div>
                          <div className="flex items-center justify-end gap-3 mt-2">
                            <button
                              onClick={() => handleUpdateQuantity(idx, -1)}
                              className="w-7 h-7 flex items-center justify-center bg-slate-800 rounded-lg text-slate-400 hover:bg-slate-700 active:scale-95 border border-slate-700"
                            >
                              <Minus size={14} />
                            </button>
                            <span className="font-bold text-sm w-4 text-center text-white">
                              {item.quantity}
                            </span>
                            <button
                              onClick={() => handleUpdateQuantity(idx, 1)}
                              className="w-7 h-7 flex items-center justify-center bg-orange-600 text-white rounded-lg active:scale-95 shadow-md shadow-orange-900/20 hover:bg-orange-500"
                            >
                              <Plus size={14} />
                            </button>
                          </div>
                        </div>
                      </div>
                    ))}
                    <div className="bg-slate-900 p-5 rounded-3xl shadow-sm border border-slate-800 mt-6 space-y-3">
                      <div className="flex justify-between text-slate-400 text-sm">
                        <span>Tạm tính ({totalItemsInCart} món)</span>
                        <span>
                          {new Intl.NumberFormat("vi-VN").format(cartTotal)}đ
                        </span>
                      </div>
                      <div className="flex justify-between text-slate-400 text-sm">
                        <span>Phí dịch vụ</span>
                        <span>0đ</span>
                      </div>
                      <div className="border-t border-dashed border-slate-700 my-2 pt-3 flex justify-between items-center">
                        <span className="font-bold text-white">
                          Tổng thanh toán
                        </span>
                        <span className="font-bold text-2xl text-orange-500">
                          {new Intl.NumberFormat("vi-VN").format(cartTotal)}đ
                        </span>
                      </div>
                    </div>
                    <div className="h-4"></div> {/* Spacer */}
                    <button
                      onClick={handlePlaceOrder}
                      disabled={isLoadingData}
                      className="w-full bg-gradient-to-r from-orange-600 to-red-600 text-white py-4 rounded-3xl font-bold text-lg shadow-lg shadow-orange-900/50 active:scale-[0.98] transition-all flex justify-center items-center gap-3 relative overflow-hidden group border border-orange-500/20"
                    >
                      <div className="absolute inset-0 bg-white/10 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
                      {isLoadingData ? (
                        <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                      ) : (
                        <>
                          <span>Xác nhận gọi món</span>
                          <ChevronRight
                            size={20}
                            className="group-hover:translate-x-1 transition-transform"
                          />
                        </>
                      )}
                    </button>
                  </div>
                )}
              </div>
            )}

            {/* VIEW: STATUS */}
            {view === "status" && (
              <div className="animate-in slide-in-from-right duration-300 max-w-3xl mx-auto">
                <div className="flex items-center gap-2 mb-6">
                  <button
                    onClick={() => setView("menu")}
                    className="p-2 -ml-2 hover:bg-slate-800 rounded-full text-slate-400 hover:text-white transition-colors"
                  >
                    <ArrowLeft size={24} />
                  </button>
                  <h2 className="text-2xl font-bold text-white">
                    Trạng thái đơn
                  </h2>
                </div>

                {orders.length === 0 ? (
                  <div className="text-center py-16">
                    <Receipt
                      size={48}
                      className="mx-auto text-slate-700 mb-4"
                    />
                    <p className="text-slate-500">Bạn chưa có đơn hàng nào.</p>
                    <button
                      onClick={() => setView("menu")}
                      className="mt-4 text-orange-500 font-medium hover:underline"
                    >
                      Quay lại gọi món
                    </button>
                  </div>
                ) : (
                  <div className="space-y-6">
                    {orders.map((order, orderIdx) => {
                      const statusSteps: OrderStatus[] = [
                        "pending",
                        "preparing",
                        "ready",
                        "served",
                      ];
                      const currentStepIdx =
                        statusSteps.indexOf(order.status) === -1
                          ? 4
                          : statusSteps.indexOf(order.status);

                      return (
                        <div
                          key={order.id}
                          className="bg-slate-900 rounded-3xl shadow-lg shadow-black/20 border-t-2 border-t-orange-200/60 border-b-2 border-b-white/10 border-x border-x-slate-800 overflow-hidden"
                        >
                          {/* Header */}
                          <div className="bg-slate-950/50 px-5 py-4 border-b border-slate-800 flex justify-between items-center">
                            <div className="flex flex-col">
                              <span className="text-xs text-slate-400 font-medium">
                                MÃ ĐƠN: #{order.id.slice(-6)}
                              </span>
                              <span className="text-xs text-slate-600">
                                {new Date(order.createdAt).toLocaleTimeString(
                                  "vi-VN",
                                  { hour: "2-digit", minute: "2-digit" },
                                )}
                              </span>
                            </div>
                            <div className="bg-slate-900 px-3 py-1 rounded-lg border border-slate-700 text-xs font-bold text-white shadow-sm">
                              {new Intl.NumberFormat("vi-VN").format(
                                order.totalAmount,
                              )}
                              đ
                            </div>
                          </div>

                          {/* Timeline */}
                          <div className="px-6 py-6 bg-slate-900">
                            <div className="flex justify-between w-full relative">
                              <TimelineItem
                                active={currentStepIdx >= 0}
                                completed={currentStepIdx > 0}
                                label="Chờ nhận"
                                icon={Receipt}
                              />
                              <TimelineItem
                                active={currentStepIdx >= 1}
                                completed={currentStepIdx > 1}
                                label="Đang nấu"
                                icon={ChefHat}
                              />
                              <TimelineItem
                                active={currentStepIdx >= 2}
                                completed={currentStepIdx > 2}
                                label="Đã xong"
                                icon={CheckCircle2}
                              />
                              <TimelineItem
                                active={currentStepIdx >= 3}
                                completed={currentStepIdx >= 3}
                                label="Phục vụ"
                                icon={UtensilsCrossed}
                                isLast
                              />
                            </div>
                          </div>

                          {/* Items List */}
                          <div className="px-5 pb-5 space-y-3">
                            {order.items.map((item, idx) => (
                              <div
                                key={idx}
                                className="flex justify-between items-start text-sm bg-slate-950/50 p-3 rounded-xl border border-slate-800"
                              >
                                <div className="flex gap-3">
                                  <div className="bg-slate-800 w-6 h-6 flex items-center justify-center rounded text-xs font-bold border border-slate-700 text-white">
                                    {item.quantity}
                                  </div>
                                  <div className="flex flex-col">
                                    <span className="font-medium text-slate-200">
                                      {item.name}
                                    </span>
                                    {item.notes && (
                                      <span className="text-xs text-slate-500 italic">
                                        "{item.notes}"
                                      </span>
                                    )}
                                  </div>
                                </div>
                                <span className="text-slate-400 font-medium">
                                  {new Intl.NumberFormat("vi-VN").format(
                                    item.price * item.quantity,
                                  )}
                                  đ
                                </span>
                              </div>
                            ))}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            )}
          </main>

          {/* --- FLOATING ACTIONS --- */}
          <div className="fixed bottom-6 right-4 sm:right-6 z-40 flex flex-col gap-4 items-end pointer-events-none">
            {/* AI Assistant FAB */}
            {view === "menu" && (
              <button
                onClick={() => setIsAIChating(true)}
                className="pointer-events-auto w-14 h-14 bg-indigo-600 hover:bg-indigo-500 text-white rounded-full shadow-lg shadow-indigo-900/50 flex items-center justify-center hover:scale-110 active:scale-95 transition-all group border border-indigo-400/30"
              >
                <Sparkles
                  size={24}
                  className="group-hover:rotate-12 transition-transform"
                />
              </button>
            )}

            {/* View Cart FAB */}
            {cart.length > 0 && view === "menu" && (
              <button
                onClick={() => setView("cart")}
                className="pointer-events-auto bg-orange-600 text-white pl-4 pr-6 py-3.5 rounded-full shadow-2xl shadow-orange-900/50 flex items-center gap-3 hover:scale-105 active:scale-95 transition-all animate-in slide-in-from-bottom duration-300 border-t border-t-orange-300/50 border-b border-b-orange-700"
              >
                <div className="relative">
                  <ShoppingBag size={24} />
                  <span className="absolute -top-2 -right-2 bg-red-600 text-white text-[10px] font-bold w-5 h-5 flex items-center justify-center rounded-full border-2 border-slate-900">
                    {totalItemsInCart}
                  </span>
                </div>
                <div className="flex flex-col items-start">
                  <span className="text-[10px] text-orange-100 uppercase tracking-wide font-bold">
                    Tổng cộng
                  </span>
                  <span className="font-bold text-base leading-none">
                    {new Intl.NumberFormat("vi-VN").format(cartTotal)}đ
                  </span>
                </div>
                <div className="w-px h-8 bg-orange-400/50 mx-1"></div>
                <ChevronRight size={20} className="text-orange-100" />
              </button>
            )}
          </div>

          {/* --- MODALS --- */}
          <AIChat
            isOpen={isAIChating}
            onClose={() => setIsAIChating(false)}
            menu={MOCK_MENU}
          />

          <ItemDetailModal
            item={selectedItem}
            isOpen={isDetailOpen}
            onClose={() => {
              setIsDetailOpen(false);
              setTimeout(() => setSelectedItem(null), 300); // Wait for animation
            }}
            onAddToCart={handleAddToCart}
          />
        </>
      )}
    </div>
  );
}

export default App;
