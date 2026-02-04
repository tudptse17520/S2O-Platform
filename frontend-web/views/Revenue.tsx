
import React from 'react';
import { MOCK_PAYMENTS } from '../mockData';
import { 
  TrendingUp, 
  Download, 
  Calendar,
  CreditCard,
  Building2,
  ChevronRight
} from 'lucide-react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';

const COLORS = ['#4f46e5', '#10b981', '#f59e0b', '#ef4444'];
const PIE_DATA = [
  { name: 'Cơ bản', value: 400 },
  { name: 'Cao cấp', value: 300 },
  { name: 'Doanh nghiệp', value: 300 },
];

const RevenueView: React.FC = () => {
  const totalRev = MOCK_PAYMENTS.reduce((acc, curr) => acc + curr.amount, 0);

  // Định dạng tiền tệ chuẩn Việt Nam: X.XXX.XXX VND
  const formatVND = (amount: number) => {
    return (amount * 1000).toLocaleString('vi-VN') + ' VND';
  };

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Phân tích Doanh thu</h1>
          <p className="text-slate-500 mt-1">Theo dõi tăng trưởng và hiệu suất các gói dịch vụ.</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-semibold hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-600/20">
          <Download size={18} /> Xuất Báo cáo
        </button>
      </div>

      {/* Main Stats */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 bg-white p-8 rounded-2xl border border-slate-200 shadow-sm relative overflow-hidden">
          <div className="relative z-10">
            <h2 className="text-lg font-bold text-slate-900 mb-6">Xu hướng Đăng ký</h2>
            <div className="h-[250px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={MOCK_PAYMENTS}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                  <XAxis dataKey="paidAt" axisLine={false} tickLine={false} tick={{fill: '#94a3b8', fontSize: 12}} />
                  <YAxis axisLine={false} tickLine={false} tick={{fill: '#94a3b8', fontSize: 12}} tickFormatter={(val) => val.toLocaleString('vi-VN')} />
                  <Tooltip 
                    cursor={{fill: '#f8fafc'}}
                    contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
                    formatter={(value: number) => [formatVND(value), 'Số tiền']}
                  />
                  <Bar dataKey="amount" fill="#4f46e5" radius={[4, 4, 0, 0]} barSize={40} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
          <div className="absolute top-0 right-0 p-8">
            <div className="flex items-center gap-2 px-3 py-1.5 bg-emerald-50 text-emerald-700 rounded-full text-xs font-bold">
              <TrendingUp size={14} /> +14.2% Tăng trưởng
            </div>
          </div>
        </div>

        <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm">
          <h2 className="text-lg font-bold text-slate-900 mb-6">Phân bổ Gói dịch vụ</h2>
          <div className="h-[200px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={PIE_DATA}
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {PIE_DATA.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(val: number) => [val.toLocaleString('vi-VN'), 'Số lượng']} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="space-y-3 mt-4">
            {PIE_DATA.map((item, idx) => (
              <div key={item.name} className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2 text-slate-600">
                  <div className="w-2.5 h-2.5 rounded-full" style={{backgroundColor: COLORS[idx]}}></div>
                  {item.name}
                </div>
                <span className="font-bold text-slate-900">{item.value.toLocaleString('vi-VN')}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Transactions Table */}
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          <div className="p-6 border-b border-slate-100 flex items-center justify-between">
            <h2 className="text-lg font-bold text-slate-900">Giao dịch gần đây</h2>
            <button className="text-indigo-600 font-bold text-xs hover:underline flex items-center gap-1">
              Xem tất cả <ChevronRight size={14} />
            </button>
          </div>
          <div className="divide-y divide-slate-50">
            {MOCK_PAYMENTS.map(payment => (
              <div key={payment.paymentId} className="px-6 py-4 flex items-center justify-between hover:bg-slate-50 transition-colors">
                <div className="flex items-center gap-4">
                  <div className="p-3 bg-slate-50 rounded-xl text-slate-600">
                    <CreditCard size={20} />
                  </div>
                  <div>
                    <p className="text-sm font-bold text-slate-900">Nhà hàng #{payment.tenantId}</p>
                    <p className="text-xs text-slate-500">{payment.method} • {payment.paidAt}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm font-bold text-slate-900">{formatVND(payment.amount)}</p>
                  <p className="text-xs text-emerald-600 font-medium">Thành công</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Financial Summary */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm border-l-4 border-l-indigo-600">
            <Calendar className="text-indigo-600 mb-4" size={24} />
            <p className="text-sm text-slate-500">Mục tiêu Tháng tới</p>
            <h3 className="text-2xl font-bold mt-1">14.200.000 VND</h3>
          </div>
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm border-l-4 border-l-emerald-600">
            <TrendingUp className="text-emerald-600 mb-4" size={24} />
            <p className="text-sm text-slate-500">Tỷ suất Lợi nhuận</p>
            <h3 className="text-2xl font-bold mt-1">28,4%</h3>
          </div>
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm border-l-4 border-l-amber-600">
            <Building2 className="text-amber-600 mb-4" size={24} />
            <p className="text-sm text-slate-500">Thuê bao mới</p>
            <h3 className="text-2xl font-bold mt-1">+12</h3>
          </div>
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm border-l-4 border-l-slate-800">
            <div className="text-slate-800 mb-4 font-bold text-xl">VND</div>
            <p className="text-sm text-slate-500">Tổng doanh thu</p>
            <h3 className="text-2xl font-bold mt-1">{formatVND(totalRev)}</h3>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RevenueView;
