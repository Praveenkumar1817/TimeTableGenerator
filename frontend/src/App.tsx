import { useState, useEffect } from 'react'
import { Calendar, Users, BookOpen, Link as LinkIcon, AlertCircle, MapPin, Layers, Trash2, Maximize2, X, Printer } from 'lucide-react'

const API_URL = "http://localhost:8000/api"

export default function App() {
  const [activeTab, setActiveTab] = useState('timetable')
  const [timetable, setTimetable] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [expandedSection, setExpandedSection] = useState<string | null>(null)

  // Data states
  const [faculty, setFaculty] = useState<any[]>([])
  const [subjects, setSubjects] = useState<any[]>([])
  const [sections, setSections] = useState<any[]>([])
  const [rooms, setRooms] = useState<any[]>([])
  const [assignments, setAssignments] = useState<any[]>([])

  const deleteRecord = async (endpoint: string, id: number) => {
    if (!confirm("Are you sure you want to delete this?")) return;
    await fetch(`${API_URL}/${endpoint}/${id}`, { method: "DELETE" });
    fetchAll();
  }

  const fetchData = async (endpoint: string, setter: any) => {
    try {
      const res = await fetch(`${API_URL}/${endpoint}`)
      if (res.ok) setter(await res.json())
    } catch (e) { }
  }

  const fetchAll = () => {
    fetchData('faculty', setFaculty)
    fetchData('subjects', setSubjects)
    fetchData('sections', setSections)
    fetchData('rooms', setRooms)
    fetchData('assignments', setAssignments)
  }

  useEffect(() => { fetchAll() }, [])

  const getFacultyNames = (poolJson: string) => {
    try {
      const ids: number[] = JSON.parse(poolJson || "[]");
      return ids.map(id => faculty.find((f: any) => f.id === id)?.name || `Prof #${id}`).join(", ");
    } catch {
      return poolJson;
    }
  };

  const getLabNames = (labsJson: string) => {
    try {
      const list: any[] = JSON.parse(labsJson || "[]");
      return list.map(l => rooms.find((r: any) => r.id === l.room_id)?.name || `Room #${l.room_id}`).join(", ");
    } catch {
      return labsJson;
    }
  };

  const generateTimetable = async () => {
    setLoading(true)
    setError("")
    try {
      const res = await fetch(`${API_URL}/timetable/generate`, { method: "POST" })
      const data = await res.json()
      if (res.ok) setTimetable(data.timetable)
      else setError(data.detail)
    } catch (err: any) {
      setError("Failed to connect to backend server")
    }
    setLoading(false)
  }

  const GenericForm = ({ endpoint, fields, onAdd }: any) => {
    const [form, setForm] = useState<any>({})
    
    const handleSubmit = async (e: any) => {
      e.preventDefault()
      await fetch(`${API_URL}/${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form)
      })
      setForm({})
      onAdd()
    }

    return (
      <form onSubmit={handleSubmit} className="flex gap-4 mb-8 flex-wrap">
        {fields.map((f: any) => (
          <input
            key={f.name}
            type={f.type || "text"}
            placeholder={f.placeholder}
            value={form[f.name] || ""}
            onChange={(e) => setForm({ ...form, [f.name]: f.type === 'number' ? Number(e.target.value) : e.target.value })}
            className="flex-1 min-w-[200px] border border-slate-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
        ))}
        <button type="submit" className="bg-slate-900 hover:bg-slate-800 text-white px-6 py-2.5 rounded-lg font-medium transition-colors">
          Add Record
        </button>
      </form>
    )
  }

  const NavItem = ({ id, icon: Icon, label }: any) => (
    <button
      onClick={() => setActiveTab(id)}
      className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
        activeTab === id ? 'bg-indigo-600 text-white' : 'text-slate-300 hover:bg-slate-800'
      }`}
    >
      <Icon size={20} />
      <span className="font-medium">{label}</span>
    </button>
  )

  return (
    <div className="flex h-screen bg-slate-50 text-slate-900 font-sans">
      <aside className="w-64 bg-slate-950 text-white flex flex-col shadow-xl z-10 shrink-0">
        <div className="p-6 border-b border-slate-800 flex items-center gap-3">
          <div className="p-2 bg-indigo-600 rounded-lg"><Calendar size={24} /></div>
          <h1 className="text-xl font-bold leading-tight">Smart Timetable</h1>
        </div>
        <nav className="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
          <NavItem id="timetable" icon={Calendar} label="Timetable Engine" />
          <NavItem id="faculty" icon={Users} label="Faculty" />
          <NavItem id="subjects" icon={BookOpen} label="Subjects" />
          <NavItem id="sections" icon={Layers} label="Sections" />
          <NavItem id="rooms" icon={MapPin} label="Rooms & Labs" />
          <NavItem id="assignments" icon={LinkIcon} label="Assignments" />
        </nav>
      </aside>

      <main className="flex-1 overflow-auto flex flex-col">
        <header className="bg-white border-b border-slate-200 px-8 py-6 shadow-sm shrink-0">
          <h2 className="text-2xl font-semibold capitalize text-slate-800">
            {activeTab.replace('-', ' ')}
          </h2>
        </header>

        <div className="p-4 sm:p-6 max-w-full mx-auto w-full">
          {activeTab === 'timetable' && (
            <div className="space-y-6">
              <div className="no-print bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-medium text-slate-800">AI Optimization Engine</h3>
                  <p className="text-slate-500 text-sm mt-1">Generate a collision-free schedule using CP-SAT constraints.</p>
                </div>
                <div className="flex gap-3">
                  {timetable.length > 0 && (
                    <button onClick={() => window.print()} className="flex items-center gap-2 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 px-4 py-2.5 rounded-lg font-medium shadow-sm transition-colors cursor-pointer">
                      <Printer size={18} />
                      <span>Print PDF</span>
                    </button>
                  )}
                  <button onClick={generateTimetable} disabled={loading} className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2.5 rounded-lg font-medium shadow-sm disabled:opacity-50 transition-colors">
                    {loading ? "Computing..." : "Generate Schedule"}
                  </button>
                </div>
              </div>

              {error && (
                <div className="bg-red-50 text-red-700 p-4 rounded-lg flex items-center gap-3 border border-red-200">
                  <AlertCircle size={20} /> <p>{error}</p>
                </div>
              )}

              {timetable.length > 0 && (
                <div className="main-timetable-list space-y-8">
                  {Object.entries(
                    timetable.reduce((acc: any, curr: any) => {
                      if (!acc[curr.section]) acc[curr.section] = [];
                      acc[curr.section].push(curr);
                      return acc;
                    }, {})
                  ).map(([sectionName, entries]: [string, any]) => {
                    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
                    
                    const getCell = (d: number, p: number) => {
                      return entries.find((e: any) => e.day === d && e.period === p);
                    };

                    return (
                      <div key={sectionName} className="section-card bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
                        <div className="bg-slate-900 text-white px-4 py-2.5 font-bold text-base flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <span>{sectionName}</span>
                            <span className="text-xs font-normal text-slate-300">7 Periods / Day</span>
                          </div>
                          <button
                            onClick={() => setExpandedSection(sectionName)}
                            className="flex items-center gap-1.5 text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg border border-slate-700 transition-colors shadow-sm font-medium cursor-pointer"
                            title="Expand this section's timetable into full detailed view"
                          >
                            <Maximize2 size={13} />
                            <span>Expand View</span>
                          </button>
                        </div>
                        <div className="w-full">
                          <table className="w-full table-fixed text-center border-collapse text-xs">
                            <thead>
                              <tr className="bg-slate-100 border-b border-slate-200 text-slate-700 font-semibold">
                                <th className="w-[8%] py-2 px-1 border-r border-slate-200 text-[11px]">Day</th>
                                <th className="w-[11.5%] py-2 px-1 border-r border-slate-200 text-[11px]">P1</th>
                                <th className="w-[11.5%] py-2 px-1 border-r border-slate-200 text-[11px]">P2</th>
                                <th className="w-[4%] py-2 px-0.5 bg-slate-200/80 border-r border-slate-300 text-[9px] uppercase tracking-tighter text-slate-600">Break</th>
                                <th className="w-[11.5%] py-2 px-1 border-r border-slate-200 text-[11px]">P3</th>
                                <th className="w-[11.5%] py-2 px-1 border-r border-slate-200 text-[11px]">P4</th>
                                <th className="w-[4%] py-2 px-0.5 bg-slate-200/80 border-r border-slate-300 text-[9px] uppercase tracking-tighter text-slate-600">Lunch</th>
                                <th className="w-[11.5%] py-2 px-1 border-r border-slate-200 text-[11px]">P5</th>
                                <th className="w-[11.5%] py-2 px-1 border-r border-slate-200 text-[11px]">P6</th>
                                <th className="w-[11.5%] py-2 px-1 text-[11px]">P7</th>
                              </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-200">
                              {days.map((dayName, d) => (
                                <tr key={d} className="hover:bg-slate-50/80 text-slate-800">
                                  <td className="py-2 px-1 font-bold border-r border-slate-200 bg-slate-50 text-[11px]">
                                    {dayName.slice(0, 3)}
                                  </td>
                                  
                                  {[0, 1].map(p => {
                                    const cell = getCell(d, p);
                                    return (
                                      <td key={p} className="p-1 border-r border-slate-200 align-top h-16">
                                        {cell ? (
                                          <div className="flex flex-col gap-0.5 justify-center h-full">
                                            <span className={`font-bold leading-tight text-[11px] line-clamp-2 ${cell.subject.includes('Lab') ? 'text-emerald-700' : 'text-indigo-700'}`}>
                                              {cell.subject}
                                            </span>
                                            <span className="text-[9.5px] text-slate-500 leading-tight truncate" title={cell.faculty}>
                                              {cell.faculty}
                                            </span>
                                            {cell.room !== '-' && (
                                              <span className="text-[8.5px] bg-amber-50 text-amber-800 border border-amber-200 rounded px-1 py-0.2 mt-0.5 inline-block truncate max-w-full" title={cell.room}>
                                                {cell.room.split(' ')[0]}
                                              </span>
                                            )}
                                          </div>
                                        ) : <span className="text-slate-300 text-xs">-</span>}
                                      </td>
                                    )
                                  })}

                                  <td className="bg-slate-100/70 border-r border-slate-300 font-semibold text-slate-400 text-[9px] uppercase tracking-widest writing-mode-vertical">
                                    •
                                  </td>

                                  {[2, 3].map(p => {
                                    const cell = getCell(d, p);
                                    return (
                                      <td key={p} className="p-1 border-r border-slate-200 align-top h-16">
                                        {cell ? (
                                          <div className="flex flex-col gap-0.5 justify-center h-full">
                                            <span className={`font-bold leading-tight text-[11px] line-clamp-2 ${cell.subject.includes('Lab') ? 'text-emerald-700' : 'text-indigo-700'}`}>
                                              {cell.subject}
                                            </span>
                                            <span className="text-[9.5px] text-slate-500 leading-tight truncate" title={cell.faculty}>
                                              {cell.faculty}
                                            </span>
                                            {cell.room !== '-' && (
                                              <span className="text-[8.5px] bg-amber-50 text-amber-800 border border-amber-200 rounded px-1 py-0.2 mt-0.5 inline-block truncate max-w-full" title={cell.room}>
                                                {cell.room.split(' ')[0]}
                                              </span>
                                            )}
                                          </div>
                                        ) : <span className="text-slate-300 text-xs">-</span>}
                                      </td>
                                    )
                                  })}

                                  <td className="bg-slate-100/70 border-r border-slate-300 font-semibold text-slate-400 text-[9px] uppercase tracking-widest writing-mode-vertical">
                                    •
                                  </td>

                                  {[4, 5, 6].map(p => {
                                    const cell = getCell(d, p);
                                    return (
                                      <td key={p} className="p-1 border-r border-slate-200 align-top h-16 last:border-0">
                                        {cell ? (
                                          cell.subject === 'Association' ? (
                                            <div className="flex items-center justify-center h-full">
                                              <span className="text-[9.5px] font-semibold text-purple-700 bg-purple-50 border border-purple-200 rounded px-1.5 py-0.5">
                                                Association
                                              </span>
                                            </div>
                                          ) : (
                                            <div className="flex flex-col gap-0.5 justify-center h-full">
                                              <span className={`font-bold leading-tight text-[11px] line-clamp-2 ${cell.subject.includes('Lab') ? 'text-emerald-700' : 'text-indigo-700'}`}>
                                                {cell.subject}
                                              </span>
                                              <span className="text-[9.5px] text-slate-500 leading-tight truncate" title={cell.faculty}>
                                                {cell.faculty}
                                              </span>
                                              {cell.room !== '-' && (
                                                <span className="text-[8.5px] bg-amber-50 text-amber-800 border border-amber-200 rounded px-1 py-0.2 mt-0.5 inline-block truncate max-w-full" title={cell.room}>
                                                  {cell.room.split(' ')[0]}
                                                </span>
                                              )}
                                            </div>
                                          )
                                        ) : (
                                          <div className="flex items-center justify-center h-full">
                                            <span className="text-slate-300 text-xs">-</span>
                                          </div>
                                        )}
                                      </td>
                                    )
                                  })}

                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      </div>
                    )
                  })}
                </div>
              )}

              {/* Expanded Section Timetable Modal */}
              {expandedSection && (
                <div 
                  className="modal-backdrop fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 sm:p-6"
                  onClick={() => setExpandedSection(null)}
                >
                  <div 
                    className="modal-dialog bg-white rounded-2xl shadow-2xl max-w-6xl w-full max-h-[92vh] flex flex-col overflow-hidden border border-slate-200"
                    onClick={(e) => e.stopPropagation()}
                  >
                    <div className="bg-slate-900 text-white px-6 py-4 flex items-center justify-between shrink-0">
                      <div>
                        <h3 className="text-xl font-bold flex items-center gap-3">
                          <span>{expandedSection}</span>
                          <span className="text-xs font-normal bg-indigo-600 px-2.5 py-0.5 rounded-full text-white">Full Focus View</span>
                        </h3>
                        <p className="text-xs text-slate-400 mt-0.5">Expanded 7-period weekly schedule with complete subject, room, and faculty details</p>
                      </div>
                      <div className="flex items-center gap-3">
                        <button
                          onClick={() => window.print()}
                          className="flex items-center gap-1.5 bg-slate-800 hover:bg-slate-700 text-xs px-3 py-2 rounded-lg border border-slate-700 text-slate-200 transition-colors cursor-pointer"
                        >
                          <Printer size={14} />
                          <span>Print</span>
                        </button>
                        <button
                          onClick={() => setExpandedSection(null)}
                          className="bg-slate-800 hover:bg-slate-700 p-2 rounded-lg text-slate-300 hover:text-white transition-colors cursor-pointer"
                          title="Close"
                        >
                          <X size={18} />
                        </button>
                      </div>
                    </div>

                    <div className="p-6 overflow-auto flex-1 bg-slate-50/50">
                      {(() => {
                        const secEntries = timetable.filter((e: any) => e.section === expandedSection);
                        const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
                        const getSecCell = (d: number, p: number) => secEntries.find((e: any) => e.day === d && e.period === p);

                        return (
                          <table className="w-full table-fixed text-center border-collapse border border-slate-200 rounded-xl overflow-hidden shadow-sm bg-white">
                            <thead>
                              <tr className="bg-slate-100 border-b border-slate-200 text-slate-700 font-bold text-xs uppercase tracking-wider">
                                <th className="w-[10%] py-3.5 px-2 border-r border-slate-200">Day</th>
                                <th className="w-[11%] py-3.5 px-2 border-r border-slate-200">Period 1</th>
                                <th className="w-[11%] py-3.5 px-2 border-r border-slate-200">Period 2</th>
                                <th className="w-[5%] py-3.5 px-1 bg-slate-200 border-r border-slate-300 text-[10px] text-slate-600">Break</th>
                                <th className="w-[11%] py-3.5 px-2 border-r border-slate-200">Period 3</th>
                                <th className="w-[11%] py-3.5 px-2 border-r border-slate-200">Period 4</th>
                                <th className="w-[5%] py-3.5 px-1 bg-slate-200 border-r border-slate-300 text-[10px] text-slate-600">Lunch</th>
                                <th className="w-[11%] py-3.5 px-2 border-r border-slate-200">Period 5</th>
                                <th className="w-[11%] py-3.5 px-2 border-r border-slate-200">Period 6</th>
                                <th className="w-[11%] py-3.5 px-2">Period 7</th>
                              </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-200 text-sm">
                              {days.map((dayName, d) => (
                                <tr key={d} className="hover:bg-slate-50 text-slate-800">
                                  <td className="py-4 px-2 font-bold border-r border-slate-200 bg-slate-50 text-slate-900">
                                    {dayName}
                                  </td>

                                  {[0, 1].map(p => {
                                    const cell = getSecCell(d, p);
                                    return (
                                      <td key={p} className="p-2.5 border-r border-slate-200 align-top h-24">
                                        {cell ? (
                                          <div className="flex flex-col gap-1 justify-center h-full">
                                            <span className={`font-bold text-xs leading-snug ${cell.subject.includes('Lab') ? 'text-emerald-700' : 'text-indigo-700'}`}>
                                              {cell.subject}
                                            </span>
                                            <span className="text-[11px] text-slate-600 font-medium leading-tight">
                                              {cell.faculty}
                                            </span>
                                            {cell.room !== '-' && (
                                              <span className="text-[10px] bg-amber-50 text-amber-800 border border-amber-200 rounded px-1.5 py-0.5 mt-1 inline-block w-max mx-auto">
                                                {cell.room}
                                              </span>
                                            )}
                                          </div>
                                        ) : <span className="text-slate-300">-</span>}
                                      </td>
                                    );
                                  })}

                                  <td className="bg-slate-100 border-r border-slate-300 font-bold text-slate-400 text-xs uppercase tracking-widest">
                                    Break
                                  </td>

                                  {[2, 3].map(p => {
                                    const cell = getSecCell(d, p);
                                    return (
                                      <td key={p} className="p-2.5 border-r border-slate-200 align-top h-24">
                                        {cell ? (
                                          <div className="flex flex-col gap-1 justify-center h-full">
                                            <span className={`font-bold text-xs leading-snug ${cell.subject.includes('Lab') ? 'text-emerald-700' : 'text-indigo-700'}`}>
                                              {cell.subject}
                                            </span>
                                            <span className="text-[11px] text-slate-600 font-medium leading-tight">
                                              {cell.faculty}
                                            </span>
                                            {cell.room !== '-' && (
                                              <span className="text-[10px] bg-amber-50 text-amber-800 border border-amber-200 rounded px-1.5 py-0.5 mt-1 inline-block w-max mx-auto">
                                                {cell.room}
                                              </span>
                                            )}
                                          </div>
                                        ) : <span className="text-slate-300">-</span>}
                                      </td>
                                    );
                                  })}

                                  <td className="bg-slate-100 border-r border-slate-300 font-bold text-slate-400 text-xs uppercase tracking-widest">
                                    Lunch
                                  </td>

                                  {[4, 5, 6].map(p => {
                                    const cell = getSecCell(d, p);
                                    return (
                                      <td key={p} className="p-2.5 border-r border-slate-200 align-top h-24 last:border-0">
                                        {cell ? (
                                          cell.subject === 'Association' ? (
                                            <div className="flex items-center justify-center h-full">
                                              <span className="text-xs font-bold text-purple-700 bg-purple-100 border border-purple-300 rounded px-2.5 py-1">
                                                Association
                                              </span>
                                            </div>
                                          ) : (
                                            <div className="flex flex-col gap-1 justify-center h-full">
                                              <span className={`font-bold text-xs leading-snug ${cell.subject.includes('Lab') ? 'text-emerald-700' : 'text-indigo-700'}`}>
                                                {cell.subject}
                                              </span>
                                              <span className="text-[11px] text-slate-600 font-medium leading-tight">
                                                {cell.faculty}
                                              </span>
                                              {cell.room !== '-' && (
                                                <span className="text-[10px] bg-amber-50 text-amber-800 border border-amber-200 rounded px-1.5 py-0.5 mt-1 inline-block w-max mx-auto">
                                                  {cell.room}
                                                </span>
                                              )}
                                            </div>
                                          )
                                        ) : <span className="text-slate-300">-</span>}
                                      </td>
                                    );
                                  })}

                                </tr>
                              ))}
                            </tbody>
                          </table>
                        );
                      })()}
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'faculty' && (
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
              <GenericForm endpoint="faculty" fields={[{ name: "name", placeholder: "Faculty Name" }]} onAdd={fetchAll} />
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {faculty.map((f: any) => (
                  <div key={f.id} className="flex justify-between items-center gap-3 p-4 border rounded-lg bg-slate-50">
                     <span className="font-medium text-slate-700">{f.name}</span>
                     <button onClick={() => deleteRecord('faculty', f.id)} className="text-red-500 hover:text-red-700 p-1"><Trash2 size={18}/></button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'subjects' && (
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 space-y-6">
              <GenericForm endpoint="subjects" fields={[
                { name: "name", placeholder: "Subject Name (e.g. Data Structures)" },
                { name: "code", placeholder: "Code (e.g. CS101)" },
                { name: "type", placeholder: "Type (THEORY or LAB)" },
                { name: "weekly_periods", placeholder: "Weekly Periods", type: "number" }
              ]} onAdd={fetchAll} />

              <div className="space-y-6">
                {sections.map((sec: any) => {
                  const secAssigns = assignments.filter((a: any) => a.section_id === sec.id);
                  const secSubIds = new Set(secAssigns.map((a: any) => a.subject_id));
                  const secSubs = subjects.filter((s: any) => secSubIds.has(s.id));
                  if (secSubs.length === 0) return null;

                  const totalPeriods = secSubs.reduce((acc: number, s: any) => acc + (s.weekly_periods || 0), 0);

                  return (
                    <div key={sec.id} className="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
                      <div className="bg-slate-100 px-4 py-3 border-b border-slate-200 flex justify-between items-center">
                        <h4 className="font-bold text-slate-800 text-base">{sec.name}</h4>
                        <span className="text-xs font-semibold text-slate-600 bg-white px-3 py-1 rounded-full border border-slate-200">
                          {secSubs.length} Subjects • {totalPeriods} Hours/Week
                        </span>
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 p-4 bg-white">
                        {secSubs.map((s: any) => (
                          <div key={s.id} className="flex justify-between items-start p-3 border rounded-lg bg-slate-50 hover:bg-slate-100/60 transition-colors">
                            <div>
                              <div className="font-semibold text-slate-900 text-sm flex items-center gap-2">
                                <span>{s.name}</span>
                                {s.code && <span className="text-xs font-normal text-slate-500">({s.code})</span>}
                              </div>
                              <div className="text-xs mt-1.5 text-slate-500 flex items-center gap-2">
                                <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${s.type === 'LAB' ? 'bg-emerald-100 text-emerald-800' : 'bg-indigo-100 text-indigo-800'}`}>
                                  {s.type}
                                </span>
                                <span>{s.weekly_periods} Periods/Week</span>
                              </div>
                            </div>
                            <button onClick={() => deleteRecord('subjects', s.id)} className="text-red-500 hover:text-red-700 p-1.5 hover:bg-red-50 rounded-md">
                              <Trash2 size={16}/>
                            </button>
                          </div>
                        ))}
                      </div>
                    </div>
                  );
                })}

                {(() => {
                  const assignedSubIds = new Set(assignments.map((a: any) => a.subject_id));
                  const unassigned = subjects.filter((s: any) => !assignedSubIds.has(s.id));
                  if (unassigned.length === 0) return null;
                  return (
                    <div className="border border-dashed border-slate-300 rounded-xl overflow-hidden">
                      <div className="bg-slate-50 px-4 py-3 border-b border-slate-200 font-semibold text-slate-600 text-sm">
                        Other / Unassigned Subjects ({unassigned.length})
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 p-4">
                        {unassigned.map((s: any) => (
                          <div key={s.id} className="flex justify-between items-start p-3 border rounded-lg bg-white">
                            <div>
                              <div className="font-semibold text-slate-900 text-sm">{s.name}</div>
                              <div className="text-xs mt-1 text-slate-500">{s.type} • {s.weekly_periods} Periods/Week</div>
                            </div>
                            <button onClick={() => deleteRecord('subjects', s.id)} className="text-red-500 hover:text-red-700 p-1">
                              <Trash2 size={16}/>
                            </button>
                          </div>
                        ))}
                      </div>
                    </div>
                  );
                })()}
              </div>
            </div>
          )}

          {activeTab === 'sections' && (
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
              <GenericForm endpoint="sections" fields={[{ name: "name", placeholder: "Section Name (e.g. Year 1 - CSE-A)" }]} onAdd={fetchAll} />
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {sections.map((s: any) => (
                  <div key={s.id} className="flex justify-between items-center p-4 border rounded-lg bg-slate-50 font-medium">
                     {s.name}
                     <button onClick={() => deleteRecord('sections', s.id)} className="text-red-500 hover:text-red-700 p-1"><Trash2 size={18}/></button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'rooms' && (
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
              <GenericForm endpoint="rooms" fields={[
                { name: "name", placeholder: "Room Name (e.g. 101 or DB Lab 1)" },
                { name: "capacity", placeholder: "Capacity", type: "number" }
              ]} onAdd={fetchAll} />
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {rooms.map((r: any) => (
                  <div key={r.id} className="flex justify-between items-center p-4 border rounded-lg bg-slate-50 font-medium">
                     <span>{r.name} - Cap: {r.capacity}</span>
                     <button onClick={() => deleteRecord('rooms', r.id)} className="text-red-500 hover:text-red-700 p-1"><Trash2 size={18}/></button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'assignments' && (
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
              <form onSubmit={async (e: any) => {
                e.preventDefault();
                const fd = new FormData(e.target);
                
                const facIds = fd.getAll("faculties").map(Number);
                const facPool = JSON.stringify(facIds);

                const roomIds = fd.getAll("rooms").map(Number);
                const eligibleLabs = JSON.stringify(roomIds.map(id => ({ room_id: id, priority: 1 })));

                await fetch(`${API_URL}/assignments`, {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({
                    section_id: Number(fd.get("sec_id")),
                    subject_id: Number(fd.get("sub_id")),
                    required_faculty: Number(fd.get("req_fac")),
                    faculty_pool: facPool,
                    eligible_labs: eligibleLabs
                  })
                });
                e.target.reset();
                fetchAll();
              }} className="flex flex-col gap-4 mb-8 max-w-3xl">
                
                <div className="flex gap-4">
                  <select name="sec_id" className="flex-1 border border-slate-300 rounded-lg px-4 py-2 bg-white" required>
                    <option value="">-- Select Section --</option>
                    {sections.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
                  </select>
                  <select name="sub_id" className="flex-1 border border-slate-300 rounded-lg px-4 py-2 bg-white" required>
                    <option value="">-- Select Subject --</option>
                    {subjects.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
                  </select>
                  <input name="req_fac" type="number" placeholder="Req. Faculty" defaultValue={1} className="w-32 border border-slate-300 rounded-lg px-4 py-2" required title="Number of faculty required" />
                </div>
                
                <div className="flex gap-4">
                  <div className="flex-1">
                    <label className="block text-sm font-medium text-slate-700 mb-1">Assign Faculty (Hold Ctrl/Cmd for multiple)</label>
                    <select name="faculties" multiple className="w-full border border-slate-300 rounded-lg px-4 py-2 bg-white" size={4}>
                      {faculty.map(f => <option key={f.id} value={f.id}>{f.name}</option>)}
                    </select>
                  </div>
                  <div className="flex-1">
                    <label className="block text-sm font-medium text-slate-700 mb-1">Eligible Lab Rooms (Optional)</label>
                    <select name="rooms" multiple className="w-full border border-slate-300 rounded-lg px-4 py-2 bg-white" size={4}>
                      {rooms.map(r => <option key={r.id} value={r.id}>{r.name} (Cap: {r.capacity})</option>)}
                    </select>
                  </div>
                </div>

                <button type="submit" className="bg-slate-900 hover:bg-slate-800 text-white px-6 py-2.5 rounded-lg font-medium self-start mt-2">
                  Map Subject to Section
                </button>
              </form>

              <div className="space-y-6">
                {sections.map((sec: any) => {
                  const secAssigns = assignments.filter((a: any) => a.section_id === sec.id);
                  if (secAssigns.length === 0) return null;

                  return (
                    <div key={sec.id} className="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
                      <div className="bg-slate-100 px-4 py-3 border-b border-slate-200 flex justify-between items-center">
                        <h4 className="font-bold text-slate-800 text-base">{sec.name}</h4>
                        <span className="text-xs font-semibold text-slate-600 bg-white px-3 py-1 rounded-full border border-slate-200">
                          {secAssigns.length} Allocations
                        </span>
                      </div>
                      <div className="divide-y divide-slate-100 bg-white">
                        {secAssigns.map((a: any) => {
                          const sub = subjects.find((s: any) => s.id === a.subject_id);
                          const facNames = getFacultyNames(a.faculty_pool);
                          const labNames = getLabNames(a.eligible_labs);

                          return (
                            <div key={a.id} className="p-4 hover:bg-slate-50 flex items-center justify-between text-sm transition-colors">
                              <div className="flex-1 pr-4">
                                <div className="flex items-center gap-2">
                                  <span className={`font-semibold text-base ${sub?.type === 'LAB' ? 'text-emerald-700' : 'text-indigo-700'}`}>
                                    {sub?.name || `Subject #${a.subject_id}`}
                                  </span>
                                  <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded ${sub?.type === 'LAB' ? 'bg-emerald-100 text-emerald-800' : 'bg-indigo-100 text-indigo-800'}`}>
                                    {sub?.type || 'THEORY'} • {sub?.weekly_periods || 0}h
                                  </span>
                                </div>
                                <div className="text-xs text-slate-600 mt-2 flex flex-wrap items-center gap-x-6 gap-y-1">
                                  <div>
                                    <span className="text-slate-400 font-medium">Faculty: </span>
                                    <span className="font-semibold text-slate-800">{facNames || 'None'}</span>
                                    {a.required_faculty > 1 && (
                                      <span className="ml-1.5 text-[10px] bg-slate-200 text-slate-700 px-1.5 py-0.5 rounded font-bold">
                                        {a.required_faculty} Req
                                      </span>
                                    )}
                                  </div>
                                  {labNames && (
                                    <div>
                                      <span className="text-slate-400 font-medium">Lab Venue: </span>
                                      <span className="font-semibold text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                                        {labNames}
                                      </span>
                                    </div>
                                  )}
                                </div>
                              </div>
                              <button onClick={() => deleteRecord('assignments', a.id)} className="text-red-500 hover:text-red-700 p-2 hover:bg-red-50 rounded-lg shrink-0">
                                <Trash2 size={18}/>
                              </button>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
