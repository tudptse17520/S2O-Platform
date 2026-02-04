
import React, { useState } from 'react';
import { MOCK_AI_CONFIG } from '../mockData';
import { AIConfig } from '../types';
import { 
  Bot, 
  Save, 
  RotateCcw, 
  Zap, 
  Info,
  Layers,
  Thermometer,
  Activity,
  MessageSquare,
  Search,
  Database,
  FileText,
  CheckCircle2,
  Settings,
  History,
  Heart,
  MapPin,
  Clock,
  Trash2,
  Plus
} from 'lucide-react';

interface AIConfigProps {
  onNotify: (message: string, type?: 'info' | 'success' | 'warning') => void;
}

const AIConfigView: React.FC<AIConfigProps> = ({ onNotify }) => {
  const [config, setConfig] = useState<AIConfig>(MOCK_AI_CONFIG);
  const [activeTab, setActiveTab] = useState<'chatbot' | 'recommendation'>('chatbot');
  const [isSaving, setIsSaving] = useState(false);
  
  const [documents, setDocuments] = useState([
    { id: 1, name: 'Menu_Cac_Nha_Hang_2024.pdf', size: '2.4 MB', status: 'Đã sẵn sàng' },
    { id: 2, name: 'Chinh_Sach_Khuyen_Mai.csv', size: '156 KB', status: 'Đã sẵn sàng' },
    { id: 3, name: 'Huong_Dan_Dat_Ban.txt', size: '12 KB', status: 'Đang tải lên' },
  ]);

  const handleSave = () => {
    setIsSaving(true);
    onNotify("Đang đồng bộ cấu hình AI lên server...", "info");
    setTimeout(() => {
      setIsSaving(false);
      onNotify("Đã cập nhật cấu hình thông minh thành công!", "success");
    }, 1200);
  };

  const handleToggleAI = () => {
    const newState = !config.isEnabled;
    setConfig({...config, isEnabled: newState});
    onNotify(`Hệ thống AI đã ${newState ? 'được kích hoạt' : 'tạm dừng'}`, newState ? "success" : "warning");
  };

  const handleDeleteDocument = (id: number, name: string) => {
    if (confirm(`Bạn có chắc muốn xóa tài liệu "${name}"?`)) {
      setDocuments(prev => prev.filter(doc => doc.id !== id));
      onNotify(`Đã xóa tài liệu: ${name}`, "warning");
    }
  };

  const handleAddDocument = () => {
    const newDoc = {
      id: Date.now(),
      name: `Tài_liệu_mới_${documents.length + 1}.pdf`,
      size: '0 KB',
      status: 'Đang tải lên'
    };
    setDocuments(prev => [...prev, newDoc]);
    onNotify(`Đang tải lên tài liệu: ${newDoc.name}`, "info");
    setTimeout(() => {
        setDocuments(prev => prev.map(d => d.id === newDoc.id ? {...d, status: 'Đã sẵn sàng', size: '1.2 MB'} : d));
        onNotify(`Đã nạp thành công tài liệu: ${newDoc.name}`, "success");
    }, 2500);
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-12">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Trung tâm Điều khiển AI</h1>
          <p className="text-slate-500 mt-1">Tinh chỉnh cách AI trò chuyện và gợi ý nhà hàng cho khách hàng.</p>
        </div>
        <div className="flex items-center gap-4">
           <div className={`px-4 py-2 rounded-full text-xs font-bold uppercase tracking-wider flex items-center gap-2 ${config.isEnabled ? 'bg-emerald-50 text-emerald-600' : 'bg-slate-100 text-slate-500'}`}>
             <div className={`w-2 h-2 rounded-full ${config.isEnabled ? 'bg-emerald-500 animate-pulse' : 'bg-slate-400'}`}></div>
             {config.isEnabled ? 'AI Đang Hoạt Động' : 'AI Đang Nghỉ'}
           </div>
           <button 
            onClick={handleToggleAI}
            className={`px-4 py-2 rounded-lg text-sm font-bold transition-all ${config.isEnabled ? 'bg-rose-50 text-rose-600 hover:bg-rose-100' : 'bg-indigo-600 text-white hover:bg-indigo-700'}`}
          >
            {config.isEnabled ? 'Tạm dừng AI' : 'Kích hoạt AI'}
          </button>
        </div>
      </div>

      <div className="flex gap-2 p-1 bg-slate-100 rounded-xl w-fit">
        <button 
          onClick={() => setActiveTab('chatbot')}
          className={`flex items-center gap-2 px-6 py-2.5 rounded-lg text-sm font-bold transition-all ${activeTab === 'chatbot' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
        >
          <MessageSquare size={18} /> Trợ lý ảo (Chatbot)
        </button>
        <button 
          onClick={() => setActiveTab('recommendation')}
          className={`flex items-center gap-2 px-6 py-2.5 rounded-lg text-sm font-bold transition-all ${activeTab === 'recommendation' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
        >
          <Search size={18} /> Gợi ý món ngon (AI)
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          {activeTab === 'chatbot' ? (
            <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden animate-in fade-in slide-in-from-bottom-2 duration-300">
              <div className="p-6 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-indigo-50 text-indigo-600 rounded-lg">
                    <Bot size={20} />
                  </div>
                  <h2 className="text-lg font-bold">Cài đặt Trợ lý ảo</h2>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">ĐANG SỬ DỤNG DỮ LIỆU RIÊNG</span>
                  <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
                </div>
              </div>

              <div className="p-8 space-y-8">
                <div className="grid grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <label className="text-sm font-bold text-slate-700">Bộ não xử lý chính</label>
                    <select 
                      className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm outline-none focus:ring-2 focus:ring-indigo-500/20"
                      value={config.chatbot.model}
                      onChange={(e) => {
                        setConfig({...config, chatbot: {...config.chatbot, model: e.target.value}});
                        onNotify(`Đã đổi mô hình sang: ${e.target.value}`, "info");
                      }}
                    >
                      <option value="gemini-3-flash-preview">Mô hình nhanh (Flash)</option>
                      <option value="gemini-3-pro-preview">Mô hình thông minh nhất (Pro)</option>
                    </select>
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-bold text-slate-700">Độ chi tiết khi tìm tài liệu</label>
                    <input 
                      type="number"
                      className="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm outline-none"
                      value={config.chatbot.topK}
                      onChange={(e) => setConfig({...config, chatbot: {...config.chatbot, topK: parseInt(e.target.value)}})}
                    />
                  </div>
                </div>

                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <label className="text-sm font-bold text-slate-700 flex items-center gap-2">
                      <Thermometer size={16} /> Độ "phiêu" khi trò chuyện (Sáng tạo)
                    </label>
                    <span className="text-xs font-bold text-indigo-600 bg-indigo-50 px-2 py-1 rounded">{config.chatbot.temperature}</span>
                  </div>
                  <input 
                    type="range" min="0" max="1" step="0.1" 
                    className="w-full h-1.5 bg-slate-100 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                    value={config.chatbot.temperature}
                    onChange={(e) => setConfig({...config, chatbot: {...config.chatbot, temperature: parseFloat(e.target.value)}})}
                  />
                </div>

                <div className="pt-6 border-t border-slate-100">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                      <Database size={16} /> Kho dữ liệu nhà hàng (Tài liệu tham khảo)
                    </h3>
                    <button 
                        onClick={handleAddDocument}
                        className="text-xs font-bold text-indigo-600 hover:text-indigo-700 flex items-center gap-1"
                    >
                        <Plus size={14} /> Thêm tài liệu mới
                    </button>
                  </div>
                  <div className="space-y-3">
                    {documents.length === 0 ? (
                        <div className="py-8 text-center bg-slate-50 rounded-xl border border-dashed border-slate-200">
                            <p className="text-xs text-slate-400 italic">Chưa có tài liệu nào được nạp vào AI.</p>
                        </div>
                    ) : (
                        documents.map((doc) => (
                        <div key={doc.id} className="group flex items-center justify-between p-3 bg-slate-50 rounded-xl border border-slate-100 hover:bg-white hover:shadow-sm transition-all">
                            <div className="flex items-center gap-3">
                            <FileText size={16} className="text-slate-400" />
                            <div>
                                <p className="text-xs font-bold text-slate-700">{doc.name}</p>
                                <p className="text-[10px] text-slate-400">{doc.size}</p>
                            </div>
                            </div>
                            <div className="flex items-center gap-3">
                                <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${doc.status === 'Đã sẵn sàng' ? 'bg-emerald-50 text-emerald-600' : 'bg-amber-50 text-amber-600'}`}>
                                    {doc.status}
                                </span>
                                <button 
                                    onClick={() => handleDeleteDocument(doc.id, doc.name)}
                                    className="p-1.5 text-slate-300 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-all opacity-0 group-hover:opacity-100"
                                >
                                    <Trash2 size={14} />
                                </button>
                            </div>
                        </div>
                        ))
                    )}
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden animate-in fade-in slide-in-from-bottom-2 duration-300">
                <div className="p-6 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-indigo-50 text-indigo-600 rounded-lg">
                      <Settings size={20} />
                    </div>
                    <h2 className="text-lg font-bold">Cách AI ưu tiên gợi ý</h2>
                  </div>
                </div>
                <div className="p-8 space-y-8">
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <History size={18} className="text-slate-400" />
                        <label className="text-sm font-bold text-slate-700">Dựa trên thói quen đặt hàng cũ</label>
                      </div>
                      <span className="text-xs font-bold text-indigo-600">{(config.recommendation.orderHistoryWeight * 100).toFixed(0)}%</span>
                    </div>
                    <input 
                      type="range" min="0" max="1" step="0.01" 
                      className="w-full h-1.5 bg-slate-100 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                      value={config.recommendation.orderHistoryWeight}
                      onChange={(e) => setConfig({...config, recommendation: {...config.recommendation, orderHistoryWeight: parseFloat(e.target.value)}})}
                    />
                  </div>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <Heart size={18} className="text-slate-400" />
                        <label className="text-sm font-bold text-slate-700">Dựa trên khẩu vị & sở thích riêng</label>
                      </div>
                      <span className="text-xs font-bold text-indigo-600">{(config.recommendation.userPreferenceWeight * 100).toFixed(0)}%</span>
                    </div>
                    <input 
                      type="range" min="0" max="1" step="0.01" 
                      className="w-full h-1.5 bg-slate-100 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                      value={config.recommendation.userPreferenceWeight}
                      onChange={(e) => setConfig({...config, recommendation: {...config.recommendation, userPreferenceWeight: parseFloat(e.target.value)}})}
                    />
                  </div>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <MapPin size={18} className="text-slate-400" />
                        <label className="text-sm font-bold text-slate-700">Dựa trên khoảng cách & giờ giấc</label>
                      </div>
                      <span className="text-xs font-bold text-indigo-600">{(config.recommendation.contextWeight * 100).toFixed(0)}%</span>
                    </div>
                    <input 
                      type="range" min="0" max="1" step="0.01" 
                      className="w-full h-1.5 bg-slate-100 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                      value={config.recommendation.contextWeight}
                      onChange={(e) => setConfig({...config, recommendation: {...config.recommendation, contextWeight: parseFloat(e.target.value)}})}
                    />
                  </div>
                </div>
              </div>
            </div>
          )}

          <div className="flex items-center justify-between pt-4">
             <button 
                onClick={() => {
                  setConfig(MOCK_AI_CONFIG);
                  onNotify("Đã khôi phục cài đặt mặc định", "info");
                }}
                className="flex items-center gap-2 text-slate-500 hover:text-slate-900 transition-colors text-sm font-bold"
              >
                <RotateCcw size={16} /> Hủy bỏ các thay đổi
              </button>
              <button 
                onClick={handleSave}
                disabled={isSaving}
                className="flex items-center gap-2 px-8 py-3 bg-indigo-600 text-white rounded-xl text-sm font-bold hover:bg-indigo-700 transition-all shadow-lg shadow-indigo-600/20 disabled:opacity-50"
              >
                {isSaving ? <Activity size={18} className="animate-spin" /> : <Save size={18} />}
                {isSaving ? 'Đang lưu...' : 'Lưu cài đặt thông minh'}
              </button>
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-slate-900 rounded-3xl p-8 text-white relative overflow-hidden shadow-2xl">
            <div className="absolute top-0 right-0 p-4 opacity-10">
              <Zap size={120} strokeWidth={1} />
            </div>
            <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
              <Activity className="text-indigo-400" size={24} /> Sức khỏe Hệ thống
            </h3>
            <div className="space-y-6 relative z-10">
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-white/5 rounded-2xl border border-white/10">
                  <p className="text-[10px] text-slate-400 font-bold uppercase mb-1">Xử lý câu lệnh</p>
                  <p className="text-xl font-black">12.4k/s</p>
                </div>
                <div className="p-4 bg-white/5 rounded-2xl border border-white/10">
                  <p className="text-[10px] text-slate-400 font-bold uppercase mb-1">Dữ liệu đã nạp</p>
                  <p className="text-xl font-black">{documents.length} File</p>
                </div>
              </div>
              <button className="w-full py-3 bg-indigo-500 text-white rounded-xl text-xs font-bold hover:bg-indigo-400 transition-colors">
                Kiểm tra chi tiết hiệu suất
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIConfigView;
