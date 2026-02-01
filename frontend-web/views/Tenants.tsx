
import React, { useState } from 'react';
import { MOCK_TENANTS } from '../mockData';
import { TenantStatus, Tenant } from '../types';
import { 
  CheckCircle2, 
  XCircle, 
  Clock, 
  MoreVertical, 
  ExternalLink, 
  Filter,
  Plus
} from 'lucide-react';

interface TenantsProps {
  onNotify: (message: string, type?: 'info' | 'success' | 'warning') => void;
}

const TenantsView: React.FC<TenantsProps> = ({ onNotify }) => {
  const [tenants, setTenants] = useState<Tenant[]>(MOCK_TENANTS);

  const handleStatusChange = (id: number, name: string, newStatus: TenantStatus) => {
    setTenants(prev => prev.map(t => t.tenantId === id ? { ...t, status: newStatus } : t));
    const statusText = newStatus === TenantStatus.ACTIVE ? "kích hoạt" : "tắt";
    onNotify(`Đã ${statusText} nhà hàng: ${name}`, newStatus === TenantStatus.ACTIVE ? "success" : "warning");
  };

  const getStatusBadge = (status: TenantStatus) => {
    switch (status) {
      case TenantStatus.ACTIVE:
        return <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 ring-1 ring-inset ring-emerald-600/20"><CheckCircle2 size={14}/> Đang hoạt động</span>;
      case TenantStatus.PENDING:
        return <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-amber-50 text-amber-700 ring-1 ring-inset ring-amber-600/20"><Clock size={14}/> Chờ duyệt</span>;
      case TenantStatus.INACTIVE:
        return <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-600 ring-1 ring-inset ring-slate-400/20"><XCircle size={14}/> Ngừng hoạt động</span>;
    }
  };

  return (
    <div className="max-w-7xl auto space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Quản lý Nhà hàng</h1>
          <p className="text-slate-500 mt-1">Xem xét đăng ký, gói dịch vụ và trạng thái hoạt động của các đối tác.</p>
        </div>
        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 px-4 py-2 border border-slate-200 bg-white rounded-lg text-sm font-semibold hover:bg-slate-50 transition-colors">
            <Filter size={18} /> Lọc
          </button>
          <button 
            onClick={() => onNotify("Đang mở biểu mẫu thêm nhà hàng...", "info")}
            className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-semibold hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-600/20"
          >
            <Plus size={18} /> Thêm Nhà hàng
          </button>
        </div>
      </div>

      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200">
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Thông tin Nhà hàng</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Trạng thái</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Gói Dịch vụ</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider text-right">Hành động</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {tenants.map((tenant) => (
                <tr key={tenant.tenantId} className="hover:bg-slate-50 transition-colors">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-xl bg-indigo-50 flex items-center justify-center text-indigo-600 font-bold">
                        {tenant.name.charAt(0)}
                      </div>
                      <div>
                        <div className="text-sm font-bold text-slate-900">{tenant.name}</div>
                        <div className="text-xs text-slate-500">Mã: #{tenant.tenantId}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">{getStatusBadge(tenant.status)}</td>
                  <td className="px-6 py-4">
                    <span className="text-sm text-slate-700">{tenant.subscription?.plan || 'Không có'}</span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <div className="flex items-center justify-end gap-2">
                      {tenant.status === TenantStatus.PENDING && (
                        <button 
                          onClick={() => handleStatusChange(tenant.tenantId, tenant.name, TenantStatus.ACTIVE)}
                          className="px-3 py-1.5 bg-emerald-600 text-white rounded-lg text-xs font-bold hover:bg-emerald-700 transition-colors"
                        >
                          Duyệt
                        </button>
                      )}
                      {tenant.status === TenantStatus.ACTIVE && (
                        <button 
                          onClick={() => handleStatusChange(tenant.tenantId, tenant.name, TenantStatus.INACTIVE)}
                          className="px-3 py-1.5 bg-slate-200 text-slate-700 rounded-lg text-xs font-bold hover:bg-slate-300 transition-colors"
                        >
                          Tắt
                        </button>
                      )}
                      <button className="p-2 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100 transition-colors">
                        <ExternalLink size={18} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default TenantsView;
