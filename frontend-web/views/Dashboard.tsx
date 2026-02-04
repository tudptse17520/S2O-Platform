
import React from 'react';
import { 
  Store, 
  Users, 
  ArrowUpRight, 
  ArrowDownRight, 
  TrendingUp, 
  Activity, 
  CreditCard 
} from 'lucide-react';
import { 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  BarChart,
  Bar
} from 'recharts';

const data = [
  { name: 'Thứ 2', revenue: 4000, users: 2400 },
  { name: 'Thứ 3', revenue: 3000, users: 1398 },
  { name: 'Thứ 4', revenue: 2000, users: 9800 },
  { name: 'Thứ 5', revenue: 2780, users: 3908 },
  { name: 'Thứ 6', revenue: 1890, users: 4800 },
  { name: 'Thứ 7', revenue: 2390, users: 3800 },
  { name: 'CN', revenue: 3490, users: 4300 },
];

interface StatCardProps {
  title: string;
  value: string;
  change: string;
  isPositive: boolean;
  icon: React.ElementType;
}

const StatCard: React.FC<StatCardProps> = ({ title, value, change, isPositive, icon: Icon }) => (
  <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
    <div className="flex items-center justify-between mb-4">
      <div className="p-3 bg-slate-50 text-slate-600 rounded-xl">
        <Icon size={24} />
      </div>
      <div className={`flex items-center gap-1 text-sm font-semibold ${isPositive ? 'text-emerald-600' : 'text-rose-600'}`}>
        {isPositive ? <ArrowUpRight size={16} /> : <ArrowDownRight size={16} />}
        {change}
      </div>
    </div>
    <h3 className="text-slate-500 text-sm font-medium">{title}</h3>
    <p className="text-2xl font-bold mt-1">{value}</p>
  </div>
);

const DashboardView: React.FC<{ onNavigate: (v: any) => void }> = ({ onNavigate }) => {
  // Hàm định dạng số chuẩn Việt Nam: X.XXX.XXX VND
  const formatCurrency = (val: number) => {
    return val.toLocaleString('vi-VN') + ' VND';
  };

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Tổng quan Hệ thống</h1>
        <p className="text-slate-500 mt-1">Theo dõi hiệu suất hệ thống và các chỉ số chính trong thời gian thực.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard 
          title="Tổng doanh thu" 
          value="248.392.000 VND" 
          change="12.5%" 
          isPositive={true} 
          icon={CreditCard} 
        />
        <StatCard 
          title="Nhà hàng hoạt động" 
          value="1.284" 
          change="8.2%" 
          isPositive={true} 
          icon={Store} 
        />
        <StatCard 
          title="Người dùng nền tảng" 
          value="48.293" 
          change="3.1%" 
          isPositive={true} 
          icon={Users} 
        />
        <StatCard 
          title="T.gian phản hồi TB" 
          value="142ms" 
          change="2.4%" 
          isPositive={false} 
          icon={Activity} 
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Revenue Chart */}
        <div className="lg:col-span-2 bg-white p-8 rounded-2xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-lg font-bold text-slate-900">Tăng trưởng doanh thu</h2>
              <p className="text-sm text-slate-500">So sánh thu nhập đăng ký theo tuần</p>
            </div>
            <button 
              onClick={() => onNavigate('revenue')}
              className="text-sm font-semibold text-indigo-600 hover:text-indigo-700 flex items-center gap-1"
            >
              Báo cáo chi tiết <ArrowUpRight size={16} />
            </button>
          </div>
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data}>
                <defs>
                  <linearGradient id="colorRev" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#4f46e5" stopOpacity={0.1}/>
                    <stop offset="95%" stopColor="#4f46e5" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#94a3b8', fontSize: 12}} dy={10} />
                <YAxis axisLine={false} tickLine={false} tick={{fill: '#94a3b8', fontSize: 12}} tickFormatter={(val) => val.toLocaleString('vi-VN')} />
                <Tooltip 
                  contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
                  cursor={{ stroke: '#e2e8f0' }}
                  formatter={(value: number) => [formatCurrency(value * 1000), 'Doanh thu']}
                />
                <Area type="monotone" dataKey="revenue" stroke="#4f46e5" strokeWidth={3} fillOpacity={1} fill="url(#colorRev)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* User Stats Bar */}
        <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm">
          <div className="mb-8">
            <h2 className="text-lg font-bold text-slate-900">Đăng ký mới</h2>
            <p className="text-sm text-slate-500">Người dùng đăng ký trong 7 ngày</p>
          </div>
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#94a3b8', fontSize: 12}} />
                <Tooltip 
                  cursor={{ fill: '#f8fafc' }}
                  contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
                  formatter={(val: number) => [val.toLocaleString('vi-VN'), 'Người dùng']}
                />
                <Bar dataKey="users" fill="#94a3b8" radius={[4, 4, 0, 0]} barSize={24} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-6 flex items-center justify-between p-4 bg-slate-50 rounded-xl">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-indigo-100 text-indigo-600 rounded-lg">
                <TrendingUp size={20} />
              </div>
              <span className="text-sm font-medium">Mục tiêu ngày</span>
            </div>
            <span className="text-sm font-bold text-slate-900">Đạt 84%</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardView;
