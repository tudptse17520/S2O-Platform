
import React, { useState, useCallback, useRef, useEffect } from 'react';
import { 
  LayoutDashboard, 
  Store, 
  Users, 
  DollarSign, 
  Settings2, 
  LogOut, 
  Bell,
  Menu,
  X,
  Search,
  ChevronRight,
  ShieldCheck,
  ChefHat,
  Info,
  CheckCircle,
  AlertCircle,
  Clock
} from 'lucide-react';
import DashboardView from './views/Dashboard';
import TenantsView from './views/Tenants';
import UsersView from './views/Users';
import RevenueView from './views/Revenue';
import AIConfigView from './views/AIConfig';

export type ViewType = 'dashboard' | 'tenants' | 'users' | 'revenue' | 'ai-config';

export interface AppNotification {
  id: string;
  message: string;
  time: string;
  type: 'info' | 'success' | 'warning';
  isRead: boolean;
}

const App: React.FC = () => {
  const [activeView, setActiveView] = useState<ViewType>('dashboard');
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [notifications, setNotifications] = useState<AppNotification[]>([]);
  const [isNotiOpen, setIsNotiOpen] = useState(false);
  const notiRef = useRef<HTMLDivElement>(null);

  // Hàm thêm thông báo mới
  const addNotification = useCallback((message: string, type: AppNotification['type'] = 'info') => {
    const newNoti: AppNotification = {
      id: Date.now().toString(),
      message,
      time: new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' }),
      type,
      isRead: false
    };
    setNotifications(prev => [newNoti, ...prev].slice(0, 10)); // Giữ tối đa 10 thông báo gần nhất
  }, []);

  const markAllRead = () => {
    setNotifications(prev => prev.map(n => ({ ...n, isRead: true })));
  };

  const clearNoti = () => {
    setNotifications([]);
    setIsNotiOpen(false);
  };

  // Đóng dropdown khi click ra ngoài
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (notiRef.current && !notiRef.current.contains(event.target as Node)) {
        setIsNotiOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const unreadCount = notifications.filter(n => !n.isRead).length;

  const renderView = useCallback(() => {
    const commonProps = { onNotify: addNotification };
    switch (activeView) {
      case 'dashboard': return <DashboardView onNavigate={setActiveView} />;
      case 'tenants': return <TenantsView {...commonProps} />;
      case 'users': return <UsersView {...commonProps} />;
      case 'revenue': return <RevenueView />;
      case 'ai-config': return <AIConfigView {...commonProps} />;
      default: return <DashboardView onNavigate={setActiveView} />;
    }
  }, [activeView, addNotification]);

  return (
    <div className="flex min-h-screen bg-slate-50">
      {/* Sidebar */}
      <aside className={`fixed inset-y-0 left-0 z-50 w-64 bg-slate-900 text-white transition-transform duration-300 transform ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'} lg:relative lg:translate-x-0`}>
        <div className="flex items-center justify-between p-6 border-b border-slate-800">
          <button 
            onClick={() => {
              setActiveView('dashboard');
              addNotification("Đã quay lại Bảng điều khiển chính", "info");
            }}
            className="flex items-center gap-3 group text-left transition-opacity hover:opacity-80"
          >
            <div className="p-2.5 bg-gradient-to-br from-orange-500 to-rose-600 rounded-xl shrink-0 shadow-lg shadow-rose-900/20 ring-1 ring-white/10 group-hover:scale-105 transition-transform">
              <ChefHat size={22} className="text-white" />
            </div>
            <div className="flex flex-col leading-tight">
              <span className="text-xl font-bold tracking-wider uppercase">ANH HAI</span>
              <span className="text-[10px] text-slate-400 font-medium uppercase tracking-widest text-nowrap">Admin Restaurant</span>
            </div>
          </button>
          
          <button onClick={() => setIsSidebarOpen(false)} className="lg:hidden text-slate-400 hover:text-white">
            <X size={24} />
          </button>
        </div>

        <nav className="mt-6 px-4 space-y-2">
          {[
            { id: 'dashboard', icon: LayoutDashboard, label: 'Bảng điều khiển' },
            { id: 'tenants', icon: Store, label: 'Quản lý Nhà hàng' },
            { id: 'users', icon: Users, label: 'Tài khoản Người dùng' },
            { id: 'revenue', icon: DollarSign, label: 'Doanh thu & Báo cáo' },
            { id: 'ai-config', icon: Settings2, label: 'Cấu hình AI' },
          ].map((item) => (
            <button
              key={item.id}
              onClick={() => {
                setActiveView(item.id as ViewType);
                if (activeView !== item.id) addNotification(`Truy cập trang ${item.label}`, "info");
              }}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-colors ${activeView === item.id ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/20' : 'text-slate-400 hover:bg-slate-800 hover:text-white'}`}
            >
              <item.icon size={20} />
              {item.label}
              {activeView === item.id && <ChevronRight size={16} className="ml-auto" />}
            </button>
          ))}
        </nav>

        <div className="absolute bottom-0 w-full p-4 border-t border-slate-800">
          <div className="flex items-center gap-3 p-3 rounded-lg hover:bg-slate-800 transition-colors cursor-pointer">
            <div className="w-10 h-10 rounded-full bg-slate-700 flex items-center justify-center font-bold text-indigo-400">QT</div>
            <div className="flex-1 overflow-hidden">
              <p className="text-sm font-semibold truncate">Admin</p>
              <p className="text-xs text-slate-500 truncate">admin@anhhai.vn</p>
            </div>
            <LogOut size={18} className="text-slate-500" />
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0">
        <header className="sticky top-0 z-40 flex items-center justify-between h-20 px-8 bg-white border-b border-slate-200 shadow-sm">
          <div className="flex items-center gap-4">
            <button onClick={() => setIsSidebarOpen(true)} className="lg:hidden text-slate-500 hover:text-slate-900">
              <Menu size={24} />
            </button>
            <div className="relative hidden sm:block">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
              <input 
                type="text" 
                placeholder="Tìm kiếm tài nguyên..." 
                className="w-80 pl-10 pr-4 py-2 bg-slate-100 border-none rounded-full text-sm focus:ring-2 focus:ring-indigo-500/20 transition-all outline-none"
              />
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            {/* Notification Bell with Dropdown */}
            <div className="relative" ref={notiRef}>
              <button 
                onClick={() => {
                  setIsNotiOpen(!isNotiOpen);
                  if (!isNotiOpen) markAllRead();
                }}
                className={`relative p-2 rounded-full transition-colors ${isNotiOpen ? 'bg-indigo-50 text-indigo-600' : 'text-slate-500 hover:bg-slate-100'}`}
              >
                <Bell size={20} />
                {unreadCount > 0 && (
                  <span className="absolute top-1 right-1 w-4 h-4 bg-rose-500 text-[10px] text-white font-bold flex items-center justify-center rounded-full ring-2 ring-white">
                    {unreadCount}
                  </span>
                )}
              </button>

              {/* Dropdown Menu */}
              {isNotiOpen && (
                <div className="absolute right-0 mt-3 w-80 bg-white rounded-2xl border border-slate-200 shadow-2xl overflow-hidden animate-in fade-in slide-in-from-top-2 duration-200">
                  <div className="p-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
                    <h3 className="text-sm font-bold text-slate-900">Thông báo gần đây</h3>
                    <button onClick={clearNoti} className="text-[10px] font-bold text-slate-400 hover:text-rose-600 uppercase tracking-wider">Xóa hết</button>
                  </div>
                  <div className="max-h-96 overflow-y-auto divide-y divide-slate-50">
                    {notifications.length === 0 ? (
                      <div className="p-8 text-center">
                        <div className="w-12 h-12 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-3">
                          <Bell size={20} className="text-slate-300" />
                        </div>
                        <p className="text-xs text-slate-400 font-medium">Chưa có hoạt động nào được ghi lại.</p>
                      </div>
                    ) : (
                      notifications.map((noti) => (
                        <div key={noti.id} className="p-4 hover:bg-slate-50 transition-colors flex gap-3">
                          <div className={`mt-0.5 shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                            noti.type === 'success' ? 'bg-emerald-50 text-emerald-600' :
                            noti.type === 'warning' ? 'bg-amber-50 text-amber-600' :
                            'bg-indigo-50 text-indigo-600'
                          }`}>
                            {noti.type === 'success' ? <CheckCircle size={14}/> : noti.type === 'warning' ? <AlertCircle size={14}/> : <Info size={14}/>}
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-xs text-slate-700 leading-normal mb-1">{noti.message}</p>
                            <div className="flex items-center gap-1 text-[10px] text-slate-400">
                              <Clock size={10} /> {noti.time}
                            </div>
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                </div>
              )}
            </div>

            <div className="h-8 w-px bg-slate-200"></div>
            <div className="flex items-center gap-2 px-3 py-1.5 bg-indigo-50 text-indigo-700 rounded-full text-xs font-semibold uppercase tracking-wider">
              <ShieldCheck size={14} />
              Hệ thống Trực tuyến
            </div>
          </div>
        </header>

        <div className="flex-1 p-8 overflow-y-auto">
          {renderView()}
        </div>
      </main>
    </div>
  );
};

export default App;
