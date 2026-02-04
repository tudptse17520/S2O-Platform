
import React, { useState } from 'react';
import { MOCK_USERS } from '../mockData';
import { User } from '../types';
import { 
  Lock, 
  Unlock, 
  Shield, 
  UserPlus, 
  Mail, 
  History 
} from 'lucide-react';

interface UsersProps {
  onNotify: (message: string, type?: 'info' | 'success' | 'warning') => void;
}

const UsersView: React.FC<UsersProps> = ({ onNotify }) => {
  const [users, setUsers] = useState<User[]>(MOCK_USERS);

  // Fix: Calculate newStatus before setUsers to ensure TypeScript understands the possible values for notification
  // This avoids a closure mutation that leads to type inference errors where the compiler thinks newStatus is always 'ACTIVE'
  const toggleLock = (userId: number, email: string) => {
    const userToUpdate = users.find(u => u.userId === userId);
    if (!userToUpdate) return;

    const newStatus: 'ACTIVE' | 'LOCKED' = userToUpdate.status === 'ACTIVE' ? 'LOCKED' : 'ACTIVE';
    
    setUsers(prev => prev.map(u => 
      u.userId === userId ? { ...u, status: newStatus } : u
    ));
    
    onNotify(
      newStatus === 'LOCKED' ? `Đã khóa tài khoản: ${email}` : `Đã mở khóa tài khoản: ${email}`,
      newStatus === 'LOCKED' ? 'warning' : 'success'
    );
  };

  const getRoleLabel = (role: string) => {
    switch(role) {
      case 'ADMIN': return 'Quản trị viên';
      case 'RESTAURANT_OWNER': return 'Chủ nhà hàng';
      case 'CUSTOMER': return 'Khách hàng';
      default: return role;
    }
  }

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Danh sách Người dùng</h1>
          <p className="text-slate-500 mt-1">Quản lý quản trị viên hệ thống, chủ nhà hàng và người dùng ứng dụng.</p>
        </div>
        <button 
          onClick={() => onNotify("Đang mở trình gửi lời mời người dùng...", "info")}
          className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-semibold hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-600/20"
        >
          <UserPlus size={18} /> Mời Người dùng
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {users.map(user => (
          <div key={user.userId} className={`bg-white rounded-2xl border border-slate-200 p-6 transition-all hover:ring-2 hover:ring-indigo-500/10 ${user.status === 'LOCKED' ? 'opacity-75 grayscale shadow-inner bg-slate-50/50' : 'shadow-sm'}`}>
            <div className="flex items-start justify-between mb-4">
              <div className={`w-12 h-12 rounded-2xl flex items-center justify-center font-bold text-lg ${
                user.role === 'ADMIN' ? 'bg-indigo-50 text-indigo-600' :
                user.role === 'RESTAURANT_OWNER' ? 'bg-emerald-50 text-emerald-600' :
                'bg-slate-50 text-slate-600'
              }`}>
                {user.email.charAt(0).toUpperCase()}
              </div>
              <button 
                onClick={() => toggleLock(user.userId, user.email)}
                className={`p-2 rounded-xl transition-colors ${
                  user.status === 'ACTIVE' 
                  ? 'text-slate-400 hover:text-rose-600 hover:bg-rose-50' 
                  : 'text-rose-600 bg-rose-50 hover:text-emerald-600 hover:bg-emerald-50'
                }`}
                title={user.status === 'ACTIVE' ? 'Khóa tài khoản' : 'Mở khóa'}
              >
                {user.status === 'ACTIVE' ? <Unlock size={20} /> : <Lock size={20} />}
              </button>
            </div>
            
            <div className="space-y-4">
              <div>
                <h3 className="text-sm font-bold text-slate-900 truncate" title={user.email}>{user.email}</h3>
                <p className="text-xs text-slate-500 flex items-center gap-1 mt-0.5">
                  <Shield size={12} /> {getRoleLabel(user.role)}
                </p>
              </div>

              <div className="grid grid-cols-1 gap-2 text-xs">
                <div className="p-2 bg-slate-50 rounded-lg flex items-center gap-2 text-slate-500">
                  <History size={12} /> Lần cuối: {user.lastLogin}
                </div>
              </div>

              <button 
                onClick={() => onNotify(`Đang tải cấu hình quyền hạn cho: ${user.email}`, "info")}
                className="w-full py-2 bg-slate-50 hover:bg-slate-100 text-slate-900 rounded-xl text-xs font-bold transition-colors"
              >
                Chỉnh sửa quyền
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default UsersView;
