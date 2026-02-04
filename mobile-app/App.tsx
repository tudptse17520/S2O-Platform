import React, { useState, useEffect, useRef } from "react";
import { Scanner } from "@yudiel/react-qr-scanner";
import {
  Home,
  Search,
  History,
  User as UserIcon,
  ChefHat,
  MapPin,
  Star,
  ChevronLeft,
  Send,
  QrCode,
  Navigation,
  Clock,
  DollarSign,
  Edit,
  Trash2,
  Plus,
  LogOut,
  Lock,
  Mail,
  UserPlus,
} from "lucide-react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { Restaurant, Review, MembershipTier, ChatMessage, User } from "./types";
import { generateRestaurantResponse } from "./services/geminiService";
import { api } from "./services/api";

// --- Components ---

// 1. Navigation Bar
const BottomNav = ({
  activeTab,
  onTabChange,
}: {
  activeTab: string;
  onTabChange: (tab: string) => void;
}) => (
  <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 py-2 px-4 flex justify-between items-center z-50 safe-area-bottom">
    <button
      onClick={() => onTabChange("home")}
      className={`flex flex-col items-center p-2 ${
        activeTab === "home" ? "text-orange-500" : "text-gray-400"
      }`}
    >
      <Home size={24} />
      <span className="text-[10px] mt-1">Trang chủ</span>
    </button>
    <button
      onClick={() => onTabChange("search")}
      className={`flex flex-col items-center p-2 ${
        activeTab === "search" ? "text-orange-500" : "text-gray-400"
      }`}
    >
      <Search size={24} />
      <span className="text-[10px] mt-1">Tìm kiếm</span>
    </button>
    <div className="relative -top-5">
      <button
        onClick={() => onTabChange("qr")}
        className="bg-orange-500 text-white p-4 rounded-full shadow-lg border-4 border-white hover:bg-orange-600 transition-colors"
      >
        <QrCode size={28} />
      </button>
    </div>
    <button
      onClick={() => onTabChange("history")}
      className={`flex flex-col items-center p-2 ${
        activeTab === "history" ? "text-orange-500" : "text-gray-400"
      }`}
    >
      <Clock size={24} />
      <span className="text-[10px] mt-1">Lịch sử</span>
    </button>
    <button
      onClick={() => onTabChange("profile")}
      className={`flex flex-col items-center p-2 ${
        activeTab === "profile" ? "text-orange-500" : "text-gray-400"
      }`}
    >
      <UserIcon size={24} />
      <span className="text-[10px] mt-1">Tài khoản</span>
    </button>
  </div>
);

// 2. Membership Card Component
const MembershipCard = ({ user }: { user: User }) => {
  const getGradient = () => {
    switch (user.tier) {
      case MembershipTier.DIAMOND:
        return "from-blue-600 to-purple-600";
      case MembershipTier.GOLD:
        return "from-yellow-400 to-yellow-600";
      default:
        return "from-gray-300 to-gray-500";
    }
  };

  return (
    <div
      className={`w-full rounded-2xl p-6 bg-gradient-to-r ${getGradient()} text-white shadow-xl mb-6 relative overflow-hidden`}
    >
      <div className="absolute top-0 right-0 opacity-10 transform translate-x-4 -translate-y-4">
        <Star size={120} fill="white" />
      </div>
      <div className="relative z-10">
        <div className="flex justify-between items-start mb-8">
          <div>
            <h3 className="text-sm opacity-90 uppercase tracking-widest mb-1">
              Thành viên
            </h3>
            <h2 className="text-2xl font-bold">{user.tier}</h2>
          </div>
          <img
            src={user.avatar}
            alt="User"
            className="w-12 h-12 rounded-full border-2 border-white object-cover"
          />
        </div>
        <div className="flex justify-between items-end">
          <div>
            <p className="text-xs opacity-80 mb-1">Điểm tích lũy</p>
            <p className="text-3xl font-mono font-bold">
              {user.points.toLocaleString()}
            </p>
          </div>
          <div className="text-right">
            <p className="text-xs opacity-80 mb-1">Tổng chi tiêu</p>
            <p className="font-bold">
              {(user.totalSpent / 1000000).toFixed(1)}M đ
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

// 3. Restaurant Card
interface RestaurantCardProps {
  restaurant: Restaurant;
  onClick: () => void;
}

const RestaurantCard: React.FC<RestaurantCardProps> = ({
  restaurant,
  onClick,
}) => (
  <div
    onClick={onClick}
    className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden mb-4 active:scale-95 transition-transform duration-200"
  >
    <div className="h-40 w-full relative">
      <img
        src={restaurant.image}
        alt={restaurant.name}
        className="w-full h-full object-cover"
      />
      <div className="absolute top-2 right-2 bg-white px-2 py-1 rounded-md text-xs font-bold flex items-center shadow-sm">
        <Star size={12} className="text-yellow-400 mr-1" fill="currentColor" />
        {restaurant.rating}
      </div>
    </div>
    <div className="p-4">
      <div className="flex justify-between items-start mb-1">
        <h3 className="font-bold text-lg text-gray-800">{restaurant.name}</h3>
        <span className="text-gray-500 text-xs">{restaurant.priceRange}</span>
      </div>
      <div className="flex items-center text-gray-500 text-sm mb-2">
        <MapPin size={14} className="mr-1" />
        <span className="truncate">{restaurant.address}</span>
      </div>
      <div className="flex items-center gap-2 mt-3">
        <span className="px-2 py-1 bg-orange-50 text-orange-600 text-xs rounded-md">
          {restaurant.category}
        </span>
        {restaurant.rating > 4.5 && (
          <span className="px-2 py-1 bg-red-50 text-red-600 text-xs rounded-md">
            Đề xuất
          </span>
        )}
      </div>
    </div>
  </div>
);

// 4. Chatbot Component
const ChatBot = ({
  restaurant,
  onClose,
}: {
  restaurant: Restaurant;
  onClose: () => void;
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "1",
      role: "model",
      text: `Xin chào! Tôi là trợ lý AI của ${restaurant.name}. Tôi có thể giúp gì cho bạn?`,
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: "user",
      text: input,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    const replyText = await generateRestaurantResponse(input, restaurant);

    const botMsg: ChatMessage = {
      id: (Date.now() + 1).toString(),
      role: "model",
      text: replyText,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, botMsg]);
    setLoading(false);
  };

  return (
    <div className="fixed inset-0 z-50 bg-white flex flex-col animate-in slide-in-from-right duration-300">
      <div className="bg-white border-b border-gray-200 p-4 flex items-center shadow-sm">
        <button
          onClick={onClose}
          className="p-2 -ml-2 rounded-full hover:bg-gray-100 mr-2"
        >
          <ChevronLeft size={24} />
        </button>
        <div>
          <h2 className="font-bold text-gray-800">
            Chat với {restaurant.name}
          </h2>
          <p className="text-xs text-green-500 flex items-center">
            ● Đang hoạt động
          </p>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 bg-gray-50 space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-[80%] p-3 rounded-2xl ${
                msg.role === "user"
                  ? "bg-orange-500 text-white rounded-br-none"
                  : "bg-white text-gray-800 border border-gray-200 rounded-bl-none shadow-sm"
              }`}
            >
              <p className="text-sm">{msg.text}</p>
              <span
                className={`text-[10px] mt-1 block opacity-70 ${
                  msg.role === "user" ? "text-orange-100" : "text-gray-400"
                }`}
              >
                {msg.timestamp.toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </span>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white p-3 rounded-2xl border border-gray-200 rounded-bl-none shadow-sm">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-75"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-150"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 bg-white border-t border-gray-200 safe-area-bottom">
        <div className="flex items-center gap-2 bg-gray-100 rounded-full px-4 py-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Nhập câu hỏi..."
            className="flex-1 bg-transparent outline-none text-sm"
          />
          <button
            onClick={handleSend}
            disabled={!input.trim()}
            className="text-orange-500 disabled:opacity-50"
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
};

// 5. Auth Component
const AuthScreen = ({ onLogin }: { onLogin: (user: User) => void }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      let user;
      if (isLogin) {
        user = await api.login({ email, password });
      } else {
        user = await api.register({ email, password, name });
      }

      if (user) {
        if (user.token) localStorage.setItem("token", user.token);
        onLogin(user);
      }
    } catch (err: any) {
      setError(err.message || "Đã có lỗi xảy ra");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white flex flex-col justify-center px-8 relative overflow-hidden">
      {/* Background Decor */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-green-100 rounded-full blur-3xl -mr-32 -mt-32"></div>
      <div className="absolute bottom-0 left-0 w-64 h-64 bg-orange-100 rounded-full blur-3xl -ml-32 -mb-32"></div>

      <div className="relative z-10">
        <div className="text-center mb-10">
          <div className="flex justify-center mb-6">
            {/* Logo Mũ Đầu Bếp Admin Style */}
            <div className="flex items-center gap-3 group text-left transition-all hover:scale-105">
              <div className="p-3 bg-gradient-to-br from-orange-500 to-rose-600 rounded-2xl shrink-0 shadow-lg shadow-rose-900/20 ring-1 ring-white/10">
                <ChefHat size={32} className="text-white" />
              </div>
            </div>
          </div>
          <h1 className="text-3xl font-bold text-gray-800 tracking-tight">
            ANH HAI Restaurant
          </h1>
          <p className="text-gray-500 mt-2 text-sm">
            Authentic Vietnamese Flavors
          </p>
        </div>

        <div className="bg-white/50 backdrop-blur-sm border border-gray-100 p-6 rounded-2xl shadow-xl">
          <h2 className="text-xl font-bold mb-6 text-gray-800">
            {isLogin ? "Đăng nhập" : "Tạo tài khoản"}
          </h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            {!isLogin && (
              <div className="space-y-1">
                <label className="text-xs font-medium text-gray-600 ml-1">
                  Họ tên
                </label>
                <div className="flex items-center gap-2 bg-gray-50 p-3 rounded-xl border border-gray-200 focus-within:border-orange-500 focus-within:ring-1 focus-within:ring-orange-200 transition-all">
                  <UserPlus size={18} className="text-gray-400" />
                  <input
                    required
                    type="text"
                    placeholder="Nguyễn Văn A"
                    className="bg-transparent flex-1 outline-none text-sm"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                  />
                </div>
              </div>
            )}

            <div className="space-y-1">
              <label className="text-xs font-medium text-gray-600 ml-1">
                Email
              </label>
              <div className="flex items-center gap-2 bg-gray-50 p-3 rounded-xl border border-gray-200 focus-within:border-orange-500 focus-within:ring-1 focus-within:ring-orange-200 transition-all">
                <Mail size={18} className="text-gray-400" />
                <input
                  required
                  type="email"
                  placeholder="email@example.com"
                  className="bg-transparent flex-1 outline-none text-sm"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
            </div>

            <div className="space-y-1">
              <label className="text-xs font-medium text-gray-600 ml-1">
                Mật khẩu
              </label>
              <div className="flex items-center gap-2 bg-gray-50 p-3 rounded-xl border border-gray-200 focus-within:border-orange-500 focus-within:ring-1 focus-within:ring-orange-200 transition-all">
                <Lock size={18} className="text-gray-400" />
                <input
                  required
                  type="password"
                  placeholder="••••••••"
                  className="bg-transparent flex-1 outline-none text-sm"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </div>

            {error && (
              <p className="text-red-500 text-xs text-center">{error}</p>
            )}

            <button
              disabled={loading}
              className="w-full bg-gradient-to-r from-orange-500 to-red-500 text-white font-bold py-3.5 rounded-xl shadow-lg shadow-orange-200 active:scale-95 transition-all disabled:opacity-70 mt-4"
            >
              {loading ? "Đang xử lý..." : isLogin ? "Đăng nhập" : "Đăng ký"}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-500">
              {isLogin ? "Chưa có tài khoản?" : "Đã có tài khoản?"}
              <button
                onClick={() => setIsLogin(!isLogin)}
                className="text-orange-600 font-bold ml-1 hover:underline"
              >
                {isLogin ? "Đăng ký ngay" : "Đăng nhập"}
              </button>
            </p>
          </div>

          <div className="mt-6 text-center">
            <p className="text-xs text-gray-400">
              Tài khoản demo: admin@gmail.com / 123456
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

// --- Main App Component ---

export default function App() {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [activeTab, setActiveTab] = useState("home");
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [selectedRestaurant, setSelectedRestaurant] =
    useState<Restaurant | null>(null);
  const [showChat, setShowChat] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [reviewText, setReviewText] = useState("");
  const [rating, setRating] = useState(5);
  const [currentTable, setCurrentTable] = useState<string | null>(null); // State lưu bàn hiện tại
  const [loadingData, setLoadingData] = useState(true);

  // --- Initial Data Loading ---
  useEffect(() => {
    // 1. Load User if token exists
    const token = localStorage.getItem("token");
    if (token) {
      api
        .getUserProfile()
        .then((user) => setCurrentUser(user))
        .catch(() => localStorage.removeItem("token"));
    }

    // 2. Load Restaurants
    api.getRestaurants().then((data) => {
      setRestaurants(data);
      setLoadingData(false);
    });
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    setCurrentUser(null);
    setActiveTab("home");
  };

  // -- Helpers --
  const handleRestaurantClick = (r: Restaurant) => {
    setSelectedRestaurant(r);
  };

  const handleBack = () => {
    setSelectedRestaurant(null);
    setShowChat(false);
  };

  const submitReview = async () => {
    if (!selectedRestaurant || !currentUser) return;

    const newReview = await api.submitReview(selectedRestaurant.id, {
      userId: currentUser.id,
      rating: rating,
      comment: reviewText,
      date: new Date().toISOString().split("T")[0],
      restaurantId: selectedRestaurant.id,
    });

    // Update local UI
    const updatedRestaurant = {
      ...selectedRestaurant,
      reviews: [newReview, ...selectedRestaurant.reviews],
    };
    setSelectedRestaurant(updatedRestaurant);
    setRestaurants((prev) =>
      prev.map((r) => (r.id === r.id ? updatedRestaurant : r)),
    );
    setReviewText("");
  };

  const deleteReview = async (reviewId: string) => {
    if (!selectedRestaurant) return;
    const success = await api.deleteReview(selectedRestaurant.id, reviewId);
    if (success) {
      const updatedReviews = selectedRestaurant.reviews.filter(
        (r) => r.id !== reviewId,
      );
      const updatedRestaurant = {
        ...selectedRestaurant,
        reviews: updatedReviews,
      };
      setSelectedRestaurant(updatedRestaurant);
      setRestaurants((prev) =>
        prev.map((r) => (r.id === r.id ? updatedRestaurant : r)),
      );
    }
  };

  // -- Guard Clause: If not logged in, show auth --
  if (!currentUser) {
    return <AuthScreen onLogin={setCurrentUser} />;
  }

  if (loadingData) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-white">
        <div className="flex flex-col items-center">
          <div className="w-8 h-8 border-4 border-orange-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-gray-500 text-sm mt-2">Đang tải dữ liệu...</p>
        </div>
      </div>
    );
  }

  // -- Views --

  const renderHome = () => (
    <div className="p-4 pb-20 animate-in fade-in duration-500">
      <div className="flex justify-between items-center mb-6 pt-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">
            Xin chào, {currentUser.name.split(" ").pop()} 👋
          </h1>

          {/* --- HIỂN THỊ BÀN SAU KHI QUÉT --- */}
          {currentTable ? (
            <div className="mt-1 inline-flex items-center gap-1 bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-bold border border-green-200">
              <MapPin size={12} /> Bạn đang ngồi Bàn {currentTable}
            </div>
          ) : (
            <p className="text-gray-500 text-sm mt-1">Quét QR để chọn bàn</p>
          )}
        </div>
        <img
          src={currentUser.avatar}
          alt="Avatar"
          className="w-10 h-10 rounded-full border border-gray-200 object-cover"
        />
      </div>

      <div className="mb-6">
        <h2 className="font-bold text-lg mb-3 text-gray-800">
          Đề xuất cho bạn
        </h2>
        <div className="flex gap-4 overflow-x-auto pb-4 no-scrollbar">
          {restaurants.slice(0, 3).map((r) => (
            <div
              key={r.id}
              onClick={() => handleRestaurantClick(r)}
              className="min-w-[280px] bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden shrink-0 active:scale-95 transition-transform"
            >
              <img src={r.image} className="h-32 w-full object-cover" />
              <div className="p-3">
                <h3 className="font-bold text-gray-800">{r.name}</h3>
                <div className="flex items-center text-xs text-gray-500 mt-1">
                  <Star
                    size={12}
                    className="text-yellow-400 mr-1"
                    fill="currentColor"
                  />
                  {r.rating} • {r.category}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="mb-4">
        <h2 className="font-bold text-lg mb-3 text-gray-800">
          Tất cả nhà hàng
        </h2>
        {restaurants.map((r) => (
          <RestaurantCard
            key={r.id}
            restaurant={r}
            onClick={() => handleRestaurantClick(r)}
          />
        ))}
      </div>
    </div>
  );

  const renderSearch = () => (
    <div className="p-4 pb-20 pt-10 animate-in fade-in duration-300">
      <h1 className="text-2xl font-bold mb-4">Tìm kiếm</h1>
      <div className="bg-white p-3 rounded-xl shadow-sm border border-gray-200 mb-6 flex items-center gap-2">
        <Search className="text-gray-400" size={20} />
        <input
          type="text"
          placeholder="Tên nhà hàng, món ăn..."
          className="flex-1 outline-none text-sm"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      <div className="flex gap-2 flex-wrap mb-6">
        {["Gần đây", "Đánh giá cao", "Giá rẻ", "Món Việt", "Sushi"].map(
          (tag) => (
            <button
              key={tag}
              className="px-4 py-2 bg-gray-100 rounded-full text-xs text-gray-600 font-medium hover:bg-orange-100 hover:text-orange-600 transition-colors"
            >
              {tag}
            </button>
          ),
        )}
      </div>

      <div className="space-y-4">
        {restaurants
          .filter(
            (r) =>
              r.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
              r.category.toLowerCase().includes(searchQuery.toLowerCase()),
          )
          .map((r) => (
            <RestaurantCard
              key={r.id}
              restaurant={r}
              onClick={() => handleRestaurantClick(r)}
            />
          ))}
      </div>
    </div>
  );

  const renderHistory = () => {
    const data = currentUser.history
      .map((h) => ({
        name: h.date.slice(5), // mm-dd
        amount: h.total,
      }))
      .reverse();

    return (
      <div className="p-4 pb-20 pt-10 animate-in fade-in duration-300">
        <h1 className="text-2xl font-bold mb-6">Lịch sử chi tiêu</h1>

        <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 mb-6">
          <h3 className="text-sm text-gray-500 mb-4">Tổng quan tháng này</h3>
          <div className="h-48 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data}>
                <defs>
                  <linearGradient id="colorAmount" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#f97316" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#f97316" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                  stroke="#f0f0f0"
                />
                <XAxis
                  dataKey="name"
                  axisLine={false}
                  tickLine={false}
                  tick={{ fontSize: 10 }}
                />
                <YAxis hide />
                <Tooltip />
                <Area
                  type="monotone"
                  dataKey="amount"
                  stroke="#f97316"
                  fillOpacity={1}
                  fill="url(#colorAmount)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <h2 className="font-bold text-lg mb-4 text-gray-800">Đã ghé thăm</h2>
        <div className="space-y-4">
          {currentUser.history.map((item) => (
            <div
              key={item.id}
              className="bg-white p-4 rounded-xl border border-gray-100 flex justify-between items-center"
            >
              <div>
                <h4 className="font-bold text-gray-800">
                  {item.restaurantName}
                </h4>
                <p className="text-xs text-gray-500">
                  {item.date} • {item.items.length} món
                </p>
                <p className="text-xs text-gray-400 mt-1 truncate max-w-[200px]">
                  {item.items.join(", ")}
                </p>
              </div>
              <div className="text-right">
                <span className="block font-bold text-orange-600">
                  {item.total.toLocaleString()}đ
                </span>
                <button className="text-xs text-blue-500 mt-1">Đặt lại</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderProfile = () => (
    <div className="p-4 pb-20 pt-10 animate-in fade-in duration-300">
      <h1 className="text-2xl font-bold mb-6">Tài khoản</h1>
      <MembershipCard user={currentUser} />

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        {[
          { icon: Edit, label: "Chỉnh sửa hồ sơ" },
          { icon: MapPin, label: "Sổ địa chỉ" },
          { icon: Star, label: "Đánh giá của tôi" },
          { icon: DollarSign, label: "Phương thức thanh toán" },
        ].map((item, idx) => (
          <div
            key={idx}
            className="p-4 flex items-center justify-between border-b border-gray-50 last:border-0 active:bg-gray-50 cursor-pointer hover:bg-gray-50"
          >
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-gray-600">
                <item.icon size={16} />
              </div>
              <span className="text-sm font-medium text-gray-700">
                {item.label}
              </span>
            </div>
            <ChevronLeft size={16} className="rotate-180 text-gray-400" />
          </div>
        ))}
      </div>

      <button
        onClick={handleLogout}
        className="w-full mt-6 py-3 text-red-500 font-medium bg-red-50 rounded-xl flex items-center justify-center gap-2 hover:bg-red-100 transition-colors"
      >
        <LogOut size={18} /> Đăng xuất
      </button>
    </div>
  );

  const renderQR = () => (
    <div className="fixed inset-0 bg-black z-50 flex flex-col items-center justify-center animate-in zoom-in duration-300">
      {/* Nút quay lại */}
      <button
        onClick={() => setActiveTab("home")}
        className="absolute top-10 left-6 p-2 bg-white/20 rounded-full z-50 text-white"
      >
        <ChevronLeft size={24} />
      </button>

      <div className="w-full max-w-md aspect-square relative overflow-hidden rounded-2xl border-4 border-orange-500 shadow-2xl">
        {/* CAMERA COMPONENT */}
        <Scanner
          onScan={(result) => {
            if (result && result.length > 0) {
              const scannedData = result[0].rawValue;

              // Xử lý logic khi quét được
              // Giả sử mã QR là: "TABLE_ID:5"
              if (scannedData.includes("TABLE_ID")) {
                const tableNumber = scannedData.split(":")[1];
                setCurrentTable(tableNumber); // Lưu số bàn
                alert(`Đã nhận diện: Bàn số ${tableNumber}`);
                setActiveTab("home"); // Quay về trang chủ để gọi món
              } else {
                alert("Mã QR không hợp lệ: " + scannedData);
              }
            }
          }}
          onError={(error: any) => console.log(error?.message || error)}
          styles={{
            container: { width: "100%", height: "100%" },
          }}
        />

        {/* Khung trang trí đè lên camera */}
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-0 left-0 w-8 h-8 border-t-4 border-l-4 border-orange-500"></div>
          <div className="absolute top-0 right-0 w-8 h-8 border-t-4 border-r-4 border-orange-500"></div>
          <div className="absolute bottom-0 left-0 w-8 h-8 border-b-4 border-l-4 border-orange-500"></div>
          <div className="absolute bottom-0 right-0 w-8 h-8 border-b-4 border-r-4 border-orange-500"></div>
        </div>
      </div>

      <p className="text-lg font-medium mb-2 text-white mt-8">
        Đang quét mã QR...
      </p>
      <p className="text-sm text-gray-400 text-center px-10">
        Vui lòng hướng camera vào mã QR trên bàn để gọi món
      </p>
    </div>
  );

  const renderRestaurantDetail = () => {
    if (!selectedRestaurant) return null;

    return (
      <div className="fixed inset-0 z-40 bg-white overflow-y-auto pb-20 animate-in slide-in-from-bottom duration-300">
        {/* Header Image */}
        <div className="relative h-64">
          <img
            src={selectedRestaurant.image}
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
          <button
            onClick={handleBack}
            className="absolute top-10 left-4 p-2 bg-white/30 backdrop-blur-md rounded-full text-white hover:bg-white/40"
          >
            <ChevronLeft size={24} />
          </button>
          <div className="absolute bottom-4 left-4 text-white">
            <h1 className="text-2xl font-bold mb-1">
              {selectedRestaurant.name}
            </h1>
            <p className="text-sm opacity-90">
              {selectedRestaurant.category} • {selectedRestaurant.priceRange}
            </p>
          </div>
        </div>

        <div className="p-4 -mt-6 bg-white rounded-t-3xl relative z-10 min-h-screen">
          {/* Actions */}
          <div className="flex justify-between items-center mb-6">
            <div className="flex gap-2">
              <span className="flex items-center gap-1 bg-green-100 text-green-700 px-3 py-1 rounded-lg text-xs font-bold">
                <Star size={12} fill="currentColor" />{" "}
                {selectedRestaurant.rating}
              </span>
              <span className="flex items-center gap-1 bg-gray-100 text-gray-600 px-3 py-1 rounded-lg text-xs">
                1.2km
              </span>
            </div>
            <a
              href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
                selectedRestaurant.address,
              )}`}
              target="_blank"
              rel="noreferrer"
              className="flex items-center gap-2 text-blue-600 text-sm font-medium"
            >
              <Navigation size={16} /> Chỉ đường
            </a>
          </div>

          <div className="mb-6">
            <h3 className="font-bold text-gray-800 mb-2">Giới thiệu</h3>
            <p className="text-gray-500 text-sm leading-relaxed">
              {selectedRestaurant.description}
            </p>
          </div>

          {/* Chatbot Entry */}
          <div
            onClick={() => setShowChat(true)}
            className="mb-6 p-4 bg-gradient-to-r from-orange-50 to-orange-100 border border-orange-200 rounded-xl flex items-center justify-between cursor-pointer active:scale-95 transition-transform"
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-orange-500 rounded-full flex items-center justify-center text-white">
                <span className="text-xs font-bold">AI</span>
              </div>
              <div>
                <h4 className="font-bold text-orange-900 text-sm">
                  Trợ lý ảo nhà hàng
                </h4>
                <p className="text-orange-700 text-xs">
                  Hỏi về menu, đặt bàn...
                </p>
              </div>
            </div>
            <ChevronLeft size={20} className="rotate-180 text-orange-400" />
          </div>

          {/* Menu Preview */}
          {selectedRestaurant.menu.length > 0 && (
            <div className="mb-6">
              <h3 className="font-bold text-gray-800 mb-3">Menu nổi bật</h3>
              <div className="space-y-3">
                {selectedRestaurant.menu.map((item) => (
                  <div key={item.id} className="flex gap-3 items-center">
                    <img
                      src={item.image}
                      className="w-16 h-16 rounded-lg object-cover"
                    />
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-800">{item.name}</h4>
                      <p className="text-xs text-gray-500 line-clamp-1">
                        {item.description}
                      </p>
                      <p className="text-orange-600 font-bold text-sm mt-1">
                        {item.price.toLocaleString()}đ
                      </p>
                    </div>
                    <button className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-orange-500 active:bg-orange-200">
                      <Plus size={16} />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Reviews */}
          <div className="mb-20">
            <div className="flex justify-between items-end mb-4">
              <h3 className="font-bold text-gray-800">Đánh giá & Bình luận</h3>
              <span className="text-xs text-gray-500">
                {selectedRestaurant.reviews.length} đánh giá
              </span>
            </div>

            {/* Add Review Box */}
            <div className="mb-6 bg-gray-50 p-4 rounded-xl">
              <div className="flex gap-1 mb-2">
                {[1, 2, 3, 4, 5].map((star) => (
                  <Star
                    key={star}
                    size={20}
                    onClick={() => setRating(star)}
                    className={`${
                      star <= rating
                        ? "text-yellow-400 fill-yellow-400"
                        : "text-gray-300"
                    } cursor-pointer`}
                  />
                ))}
              </div>
              <textarea
                className="w-full p-2 text-sm border border-gray-200 rounded-lg mb-2 focus:outline-orange-500"
                placeholder="Chia sẻ trải nghiệm của bạn..."
                rows={3}
                value={reviewText}
                onChange={(e) => setReviewText(e.target.value)}
              ></textarea>
              <button
                onClick={submitReview}
                className="bg-orange-500 text-white text-xs font-bold py-2 px-4 rounded-lg w-full active:bg-orange-600"
              >
                Gửi đánh giá
              </button>
            </div>

            <div className="space-y-4">
              {selectedRestaurant.reviews.map((rv) => (
                <div
                  key={rv.id}
                  className="border-b border-gray-100 pb-4 last:border-0"
                >
                  <div className="flex justify-between items-start mb-1">
                    <div className="flex items-center gap-2">
                      <div className="w-6 h-6 bg-gray-200 rounded-full flex items-center justify-center text-xs font-bold text-gray-600">
                        {rv.userName.charAt(0)}
                      </div>
                      <span className="font-medium text-sm text-gray-800">
                        {rv.userName}
                      </span>
                    </div>
                    <span className="text-xs text-gray-400">{rv.date}</span>
                  </div>
                  <div className="flex text-yellow-400 mb-1">
                    {[...Array(rv.rating)].map((_, i) => (
                      <Star key={i} size={10} fill="currentColor" />
                    ))}
                  </div>
                  <p className="text-sm text-gray-600">{rv.comment}</p>
                  {rv.userId === currentUser.id && (
                    <button
                      onClick={() => deleteReview(rv.id)}
                      className="text-red-400 text-xs mt-2 flex items-center gap-1"
                    >
                      <Trash2 size={10} /> Xóa
                    </button>
                  )}
                </div>
              ))}
              {selectedRestaurant.reviews.length === 0 && (
                <p className="text-center text-gray-400 text-sm italic">
                  Chưa có đánh giá nào.
                </p>
              )}
            </div>
          </div>
        </div>

        {/* Sticky Action Button */}
        <div className="fixed bottom-0 left-0 right-0 p-4 bg-white border-t border-gray-100 safe-area-bottom z-20">
          <button className="w-full bg-orange-600 text-white font-bold py-3 rounded-xl shadow-lg shadow-orange-200 active:scale-95 transition-transform">
            Đặt bàn ngay
          </button>
        </div>

        {/* Chat Overlay */}
        {showChat && (
          <ChatBot
            restaurant={selectedRestaurant}
            onClose={() => setShowChat(false)}
          />
        )}
      </div>
    );
  };

  if (activeTab === "qr") return renderQR();

  return (
    <div className="min-h-screen bg-gray-50 text-gray-800 font-sans selection:bg-orange-200">
      {activeTab === "home" && renderHome()}
      {activeTab === "search" && renderSearch()}
      {activeTab === "history" && renderHistory()}
      {activeTab === "profile" && renderProfile()}

      {/* Detail Modal */}
      {selectedRestaurant && renderRestaurantDetail()}

      {/* Navigation - Hide if detail view is open */}
      {!selectedRestaurant && (
        <BottomNav activeTab={activeTab} onTabChange={setActiveTab} />
      )}
    </div>
  );
}
