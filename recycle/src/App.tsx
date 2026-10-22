import { useState, useEffect, type ReactNode } from "react"

type IconName = "home" | "scan" | "history" | "wallet" | "chart" | "settings" | "bell" | "leaf" | "arrow" | "chevron" | "bottle" | "paper" | "glass" | "close" | "nfc" | "check" | "profile"

const BRIDGE_API = "http://127.0.0.1:5000/api"

interface TrayItem {
  name: string
  status: string
  confidence: string
  ok: boolean
}

interface ActivityItem {
  date: string
  place: string
  detail: string
  weight: string
  amount: string
  icon: IconName
  color: string
}

interface BridgeState {
  bin_id: string
  machine_state: "IDLE" | "SCANNED" | "ALARM" | "DROPPING"
  latch_open: boolean
  shaker_active: boolean
  speaker_msg: string
  load_cell_weight: number
  purity: number
  is_anomaly: boolean
  tray_items: TrayItem[]
  wallet_balance: number
  month_earned: number
  total_recycled_kg: number
  co2_avoided: number
  water_saved: number
  materials_kg: { Plastic: number; Paper: number; Glass: number }
  activities: ActivityItem[]
}

const iconPaths: Record<IconName, ReactNode> = {
  home: (
    <>
      <path d="m3 10 9-7 9 7" />
      <path d="M5 9v11h14V9M9 20v-6h6v6" />
    </>
  ),
  scan: (
    <>
      <path d="M4 8V4h4M16 4h4v4M20 16v4h-4M8 20H4v-4" />
      <path d="M8 12h8M12 8v8" />
    </>
  ),
  history: (
    <>
      <path d="M3 12a9 9 0 1 0 3-6.7L3 8" />
      <path d="M3 3v5h5M12 7v5l3 2" />
    </>
  ),
  wallet: (
    <>
      <path d="M4 6.5h15a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-12a2 2 0 0 1 2-2h12" />
      <path d="M16 12h5v4h-5a2 2 0 0 1 0-4Z" />
    </>
  ),
  chart: (
    <>
      <path d="M4 20V10M10 20V4M16 20v-7M22 20H2" />
    </>
  ),
  settings: (
    <>
      <circle cx="12" cy="12" r="3" />
      <path d="M19.4 15a1.8 1.8 0 0 0 .36 2l.06.06-2.83 2.83-.06-.06a1.8 1.8 0 0 0-2-.36 1.8 1.8 0 0 0-1.1 1.65V21H9.83v-.09a1.8 1.8 0 0 0-1.1-1.65 1.8 1.8 0 0 0-2 .36l-.06.06-2.83-2.83.06-.06a1.8 1.8 0 0 0 .36-2 1.8 1.8 0 0 0-1.65-1.1H2V9.7h.09a1.8 1.8 0 0 0 1.65-1.1 1.8 1.8 0 0 0-.36-2l-.06-.06 2.83-2.83.06.06a1.8 1.8 0 0 0 2 .36A1.8 1.8 0 0 0 9.3 2.48V2h4v.09a1.8 1.8 0 0 0 1.1 1.65 1.8 1.8 0 0 0 2-.36l.06-.06 2.83 2.83-.06.06a1.8 1.8 0 0 0-.36 2 1.8 1.8 0 0 0 1.65 1.1H21v4h-.09a1.8 1.8 0 0 0-1.51 1.69Z" />
    </>
  ),
  bell: (
    <>
      <path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9M10 21h4" />
    </>
  ),
  leaf: (
    <>
      <path d="M20 4C11 4 5 8 5 14c0 3 2 5 5 5 6 0 10-6 10-15Z" />
      <path d="M4 21c2-6 7-10 13-13" />
    </>
  ),
  arrow: (
    <>
      <path d="M5 12h14M14 7l5 5-5 5" />
    </>
  ),
  chevron: <path d="m9 18 6-6-6-6" />,
  bottle: (
    <>
      <path d="M9 3h6M10 3v5l-2 3v9h8v-9l-2-3V3" />
      <path d="M8 13h8" />
    </>
  ),
  paper: (
    <>
      <path d="M6 3h9l4 4v14H6Z" />
      <path d="M15 3v5h4M9 13h7M9 17h5" />
    </>
  ),
  glass: (
    <>
      <path d="M8 3h8l-1 8a3 3 0 0 1-6 0ZM12 14v7M8 21h8" />
    </>
  ),
  close: (
    <>
      <path d="m6 6 12 12M18 6 6 18" />
    </>
  ),
  nfc: (
    <>
      <path d="M8 8a6 6 0 0 1 0 8M5 5a10 10 0 0 1 0 14M12 11a2 2 0 0 1 0 2" />
    </>
  ),
  check: <path d="m5 12 4 4L19 6" />,
  profile: (
    <>
      <circle cx="12" cy="8" r="4" />
      <path d="M4 21a8 8 0 0 1 16 0" />
    </>
  ),
}

function Icon({ name, size = 20 }: { name: IconName; size?: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {iconPaths[name]}
    </svg>
  )
}

const navItems: { label: string; icon: IconName }[] = [
  { label: "Overview", icon: "home" },
  { label: "Smart bin", icon: "scan" },
  { label: "Activity", icon: "history" },
  { label: "Wallet", icon: "wallet" },
  { label: "My impact", icon: "chart" },
]

const defaultActivities: ActivityItem[] = [
  {
    date: "Today, 9:42 AM",
    place: "Bin EC-04 · Park Lobby",
    detail: "Plastic · Glass",
    weight: "3.2 kg",
    amount: "+ RM 5.80",
    icon: "bottle",
    color: "mint",
  },
  {
    date: "12 Jun, 5:18 PM",
    place: "Bin EC-02 · Block A",
    detail: "Paper · Plastic",
    weight: "2.7 kg",
    amount: "+ RM 3.40",
    icon: "paper",
    color: "blue",
  },
  {
    date: "08 Jun, 11:06 AM",
    place: "Bin EC-04 · Park Lobby",
    detail: "Glass",
    weight: "4.1 kg",
    amount: "+ RM 6.15",
    icon: "glass",
    color: "amber",
  },
]

function App() {
  const [activeNav, setActiveNav] = useState("Overview")
  const [sessionOpen, setSessionOpen] = useState(false)
  const [sessionStep, setSessionStep] = useState<"ready" | "linked">("ready")
  const [noticeOpen, setNoticeOpen] = useState(false)
  const [confirming, setConfirming] = useState(false)

  const [bridge, setBridge] = useState<BridgeState>({
    bin_id: "BIN EC-04",
    machine_state: "IDLE",
    latch_open: false,
    shaker_active: false,
    speaker_msg: "Ready",
    load_cell_weight: 0,
    purity: 100,
    is_anomaly: false,
    tray_items: [],
    wallet_balance: 42.6,
    month_earned: 15.35,
    total_recycled_kg: 40.2,
    co2_avoided: 12.8,
    water_saved: 284,
    materials_kg: { Plastic: 18.4, Paper: 13.2, Glass: 8.6 },
    activities: defaultActivities,
  })

  // 轮询 Shared Bridge 状态
  useEffect(() => {
    const timer = setInterval(async () => {
      try {
        const res = await fetch(`${BRIDGE_API}/state`)
        if (res.ok) {
          const data = await res.json()
          setBridge(data)
        }
      } catch {
        // 离线使用默认值
      }
    }, 1200)
    return () => clearInterval(timer)
  }, [])

  const handleNavClick = (label: string) => {
    if (label === "Smart bin") {
      startSession()
    } else {
      setActiveNav(label)
    }
  }

  const startSession = () => {
    setSessionStep("ready")
    setSessionOpen(true)
  }

  const handleLinkAccount = async () => {
    setSessionStep("linked")
    try {
      await fetch(`${BRIDGE_API}/resident/link`, { method: "POST" })
    } catch {
      // ignore
    }
  }

  const handleConfirmDeposit = async () => {
    setConfirming(true)
    try {
      const res = await fetch(`${BRIDGE_API}/resident/confirm`, { method: "POST" })
      if (res.ok) {
        const result = await res.json()
        if (result.state) setBridge(result.state)
      }
    } catch {
      // ignore
    } finally {
      setConfirming(false)
    }
  }

  const handleResetTray = async () => {
    try {
      const res = await fetch(`${BRIDGE_API}/reset`, { method: "POST" })
      if (res.ok) {
        const result = await res.json()
        if (result.state) setBridge(result.state)
      }
    } catch {
      // ignore
    }
  }

  const totalMat = bridge.materials_kg.Plastic + bridge.materials_kg.Paper + bridge.materials_kg.Glass || 1

  const materials = [
    {
      name: "Plastic",
      value: `${bridge.materials_kg.Plastic.toFixed(1)} kg`,
      percent: Math.round((bridge.materials_kg.Plastic / totalMat) * 100),
      icon: "bottle" as IconName,
      color: "mint",
    },
    {
      name: "Paper",
      value: `${bridge.materials_kg.Paper.toFixed(1)} kg`,
      percent: Math.round((bridge.materials_kg.Paper / totalMat) * 100),
      icon: "paper" as IconName,
      color: "blue",
    },
    {
      name: "Glass",
      value: `${bridge.materials_kg.Glass.toFixed(1)} kg`,
      percent: Math.round((bridge.materials_kg.Glass / totalMat) * 100),
      icon: "glass" as IconName,
      color: "amber",
    },
  ]

  // 🌟 Purity <= 50 或异常时，预估金钱清零为 0.00
  const isBlocked = bridge.purity <= 50 || bridge.is_anomaly
  const estPayout = isBlocked
    ? "0.00"
    : (bridge.load_cell_weight * 10 * (bridge.purity / 100)).toFixed(2)

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">
            <Icon name="leaf" size={22} />
          </div>
          <span>EcoScan</span>
        </div>

        <nav className="main-nav" aria-label="Main navigation">
          <p className="nav-label">MAIN MENU</p>
          {navItems.map((item) => (
            <button
              className={`nav-item ${activeNav === item.label ? "active" : ""}`}
              onClick={() => handleNavClick(item.label)}
              key={item.label}
            >
              <Icon name={item.icon} />
              <span>{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <button className="nav-item" onClick={() => setActiveNav("Settings")}>
            <Icon name="settings" />
            <span>Settings</span>
          </button>

          <div className="profile">
            <div className="avatar">AM</div>
            <div className="profile-copy">
              <strong>Aina Malik</strong>
              <span>Residence 08-12</span>
            </div>
            <Icon name="chevron" size={17} />
          </div>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div>
            <h1>Good morning, Aina.</h1>
          </div>

          <div className="top-actions">
            <button
              className="icon-button"
              aria-label="Notifications"
              onClick={() => setNoticeOpen(!noticeOpen)}
            >
              <Icon name="profile" />
              <span className="notification-dot" />
            </button>

            <button className="start-button compact" onClick={startSession}>
              <Icon name="scan" />
              Start a session
            </button>
          </div>

          {noticeOpen && (
            <div className="notification-popover">
              <div className="notification-icon">
                <Icon name="check" size={17} />
              </div>
              <div>
                <strong>Weekly goal reached</strong>
                <p>You recycled {bridge.total_recycled_kg.toFixed(1)} kg total. Excellent work.</p>
              </div>
            </div>
          )}
        </header>

        {/* 1. OVERVIEW TAB VIEW */}
        {activeNav === "Overview" && (
          <div className="tab-content">
            <section className="hero-grid">
              <article className="session-card" style={{ gridColumn: "1 / -1" }}>
                <div className="session-copy">
                  <div className="live-pill">
                    <span /> {bridge.bin_id} AVAILABLE ({bridge.machine_state})
                  </div>
                  <h2>
                    Ready for your
                    <br />
                    next drop-off?
                  </h2>
                  <p>
                    Link your account, empty your recyclables, and let EcoScan take care of the sorting.
                  </p>
                  <button className="start-button" onClick={startSession}>
                    <Icon name="scan" />
                    Start recycling session
                    <Icon name="arrow" />
                  </button>
                  <span className="helper-text">Park Lobby · 2 min walk</span>
                </div>

                <div className="scanner-visual" aria-hidden="true">
                  <div className="orbit orbit-one" />
                  <div className="orbit orbit-two" />
                  <div className="scan-rays" />
                  <div className="smart-bin">
                    <div className="bin-top">
                      <span />
                    </div>
                    <div className="bin-body">
                      <div className="bin-screen">
                        <Icon name="leaf" size={16} />
                      </div>
                      <div className="bin-slot" />
                      <div className="bin-logo">
                        <Icon name="leaf" size={13} /> ECOSCAN
                      </div>
                    </div>
                  </div>
                  <div className="float-chip chip-plastic">
                    <Icon name="bottle" size={17} />
                    <span>Plastic</span>
                    <strong>Valid</strong>
                  </div>
                  <div className="float-chip chip-paper">
                    <Icon name="paper" size={17} />
                    <span>Paper</span>
                    <strong>Grade A</strong>
                  </div>
                  <div className="scan-dot dot-one" />
                  <div className="scan-dot dot-two" />
                </div>
              </article>
            </section>

            <section className="stats-grid" style={{ marginTop: "24px" }}>
              <article className="impact-card">
                <div className="card-title-row">
                  <div>
                    <p className="eyebrow">YOUR IMPACT</p>
                    <h3>Small actions, real change.</h3>
                  </div>
                  <button
                    className="text-button"
                    onClick={() => setActiveNav("My impact")}
                  >
                    View report <Icon name="arrow" size={15} />
                  </button>
                </div>

                <div className="impact-content">
                  <div className="impact-ring">
                    <svg viewBox="0 0 120 120">
                      <circle className="ring-bg" cx="60" cy="60" r="48" />
                      <circle
                        className="ring-progress"
                        cx="60"
                        cy="60"
                        r="48"
                        pathLength="100"
                      />
                    </svg>
                    <div className="ring-value">
                      <strong>{bridge.total_recycled_kg.toFixed(1)}</strong>
                      <span>kg diverted</span>
                    </div>
                  </div>

                  <div className="impact-metrics">
                    <div>
                      <span className="metric-icon">
                        <Icon name="leaf" size={18} />
                      </span>
                      <p>
                        <strong>{bridge.co2_avoided.toFixed(1)} kg</strong>
                        <small>CO₂ emissions avoided</small>
                      </p>
                    </div>
                    <div>
                      <span className="metric-icon water">≈</span>
                      <p>
                        <strong>{Math.round(bridge.water_saved)} L</strong>
                        <small>Water saved</small>
                      </p>
                    </div>
                  </div>
                </div>
              </article>
            </section>

            <section className="activity-card" style={{ marginTop: "24px" }}>
              <div className="card-title-row">
                <div>
                  <p className="eyebrow">RECENT ACTIVITY</p>
                  <h3>Your recycling log</h3>
                </div>
                <button
                  className="text-button"
                  onClick={() => setActiveNav("Activity")}
                >
                  View all <Icon name="arrow" size={15} />
                </button>
              </div>

              <div className="activity-table">
                {bridge.activities.slice(0, 3).map((activity, idx) => (
                  <div className="activity-row" key={`${activity.date}-${idx}`}>
                    <span className={`material-icon ${activity.color}`}>
                      <Icon name={activity.icon} size={19} />
                    </span>
                    <div className="activity-main">
                      <strong>{activity.place}</strong>
                      <span>{activity.date}</span>
                    </div>
                    <div className="activity-detail">
                      <strong>{activity.detail}</strong>
                      <span>AI verified</span>
                    </div>
                    <strong className="weight">{activity.weight}</strong>
                    <strong className="amount">{activity.amount}</strong>
                  </div>
                ))}
              </div>
            </section>
          </div>
        )}

        {/* 2. WALLET TAB VIEW */}
        {activeNav === "Wallet" && (
          <div className="tab-content">
            <section className="hero-grid">
              <article className="wallet-card" style={{ gridColumn: "1 / -1", maxWidth: "600px", margin: "0 auto" }}>
                <div className="card-heading">
                  <div>
                    <p className="eyebrow">AVAILABLE BALANCE</p>
                    <h3>EcoWallet</h3>
                  </div>
                  <div className="wallet-icon">
                    <Icon name="wallet" size={21} />
                  </div>
                </div>

                <div className="balance">
                  <span>RM</span> {bridge.wallet_balance.toFixed(2)}
                </div>

                <div className="balance-note">
                  <span>
                    <Icon name="arrow" size={13} />
                  </span>{" "}
                  RM {bridge.month_earned.toFixed(2)} earned this month
                </div>

                <button
                  className="withdraw-button"
                  onClick={() => alert("Withdraw feature triggered: Direct transfer to bank / Touch 'n Go eWallet")}
                >
                  Withdraw or pay bills <Icon name="chevron" size={16} />
                </button>

                <div className="wallet-footer">
                  <span>Next auto-deduct</span>
                  <strong>JMB fee · 01 Jul</strong>
                </div>
              </article>
            </section>

            <section className="activity-card" style={{ marginTop: "24px" }}>
              <div className="card-title-row">
                <div>
                  <p className="eyebrow">WALLET TRANSACTIONS</p>
                  <h3>Recycling Rewards History</h3>
                </div>
              </div>

              <div className="activity-table">
                {bridge.activities.map((activity, idx) => (
                  <div className="activity-row" key={`${activity.date}-${idx}`}>
                    <span className={`material-icon ${activity.color}`}>
                      <Icon name={activity.icon} size={19} />
                    </span>
                    <div className="activity-main">
                      <strong>{activity.place}</strong>
                      <span>{activity.date}</span>
                    </div>
                    <div className="activity-detail">
                      <strong>{activity.detail}</strong>
                      <span>Credited</span>
                    </div>
                    <strong className="amount" style={{ color: "#10B981" }}>{activity.amount}</strong>
                  </div>
                ))}
              </div>
            </section>
          </div>
        )}

        {/* 3. ACTIVITY TAB VIEW */}
        {activeNav === "Activity" && (
          <div className="tab-content">
            <section className="activity-card">
              <div className="card-title-row">
                <div>
                  <p className="eyebrow">RECYCLING HISTORY</p>
                  <h3>All Activity Records</h3>
                </div>
              </div>

              <div className="activity-table">
                {bridge.activities.map((activity, idx) => (
                  <div className="activity-row" key={`${activity.date}-${idx}`}>
                    <span className={`material-icon ${activity.color}`}>
                      <Icon name={activity.icon} size={19} />
                    </span>
                    <div className="activity-main">
                      <strong>{activity.place}</strong>
                      <span>{activity.date}</span>
                    </div>
                    <div className="activity-detail">
                      <strong>{activity.detail}</strong>
                      <span>AI Verified</span>
                    </div>
                    <strong className="weight">{activity.weight}</strong>
                    <strong className="amount">{activity.amount}</strong>
                  </div>
                ))}
              </div>
            </section>
          </div>
        )}

        {/* 4. MY IMPACT TAB VIEW */}
        {activeNav === "My impact" && (
          <div className="tab-content">
            <section className="stats-grid">
              <article className="impact-card">
                <div className="card-title-row">
                  <div>
                    <p className="eyebrow">ENVIRONMENTAL IMPACT</p>
                    <h3>Sustainability Metrics</h3>
                  </div>
                </div>

                <div className="impact-content">
                  <div className="impact-ring">
                    <svg viewBox="0 0 120 120">
                      <circle className="ring-bg" cx="60" cy="60" r="48" />
                      <circle
                        className="ring-progress"
                        cx="60"
                        cy="60"
                        r="48"
                        pathLength="100"
                      />
                    </svg>
                    <div className="ring-value">
                      <strong>{bridge.total_recycled_kg.toFixed(1)}</strong>
                      <span>kg diverted</span>
                    </div>
                  </div>

                  <div className="impact-metrics">
                    <div>
                      <span className="metric-icon">
                        <Icon name="leaf" size={18} />
                      </span>
                      <p>
                        <strong>{bridge.co2_avoided.toFixed(1)} kg</strong>
                        <small>CO₂ emissions avoided</small>
                      </p>
                    </div>
                    <div>
                      <span className="metric-icon water">≈</span>
                      <p>
                        <strong>{Math.round(bridge.water_saved)} L</strong>
                        <small>Water saved</small>
                      </p>
                    </div>
                  </div>
                </div>

                <div className="goal-row" style={{ marginTop: "20px" }}>
                  <div>
                    <strong>Monthly goal</strong>
                    <span>{bridge.total_recycled_kg.toFixed(1)} of 50 kg</span>
                  </div>
                  <div className="progress">
                    <span style={{ width: `${Math.min(100, (bridge.total_recycled_kg / 50) * 100)}%` }} />
                  </div>
                </div>

                <div style={{ marginTop: "24px" }}>
                  <p className="eyebrow" style={{ marginBottom: "12px" }}>MATERIAL BREAKDOWN</p>
                  {materials.map((material) => (
                    <div className="material-row" key={material.name}>
                      <span className={`material-icon ${material.color}`}>
                        <Icon name={material.icon} size={18} />
                      </span>
                      <div className="material-info">
                        <div>
                          <strong>{material.name}</strong>
                          <span>{material.value}</span>
                        </div>
                        <div className="material-progress">
                          <span
                            className={material.color}
                            style={{ width: `${material.percent}%` }}
                          />
                        </div>
                      </div>
                      <small>{material.percent}%</small>
                    </div>
                  ))}
                </div>
              </article>
            </section>
          </div>
        )}
      </main>

      {/* 移动端 Bottom Nav 切换 */}
      <nav className="mobile-nav" aria-label="Mobile navigation">
        {navItems.slice(0, 4).map((item) => (
          <button
            className={activeNav === item.label ? "active" : ""}
            onClick={() => handleNavClick(item.label)}
            key={item.label}
          >
            <Icon name={item.icon} size={21} />
            <span>{item.label === "Smart bin" ? "Scan" : item.label}</span>
          </button>
        ))}
      </nav>

      {/* 实时扫码/分类互动 Modal */}
      {sessionOpen && (
        <div
          className="modal-backdrop"
          role="presentation"
          onMouseDown={() => setSessionOpen(false)}
        >
          <section
            className="session-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="session-title"
            onMouseDown={(event) => event.stopPropagation()}
          >
            <button
              className="modal-close"
              aria-label="Close"
              onClick={() => setSessionOpen(false)}
            >
              <Icon name="close" />
            </button>

            {sessionStep === "ready" ? (
              <>
                <div className="modal-icon">
                  <Icon name="nfc" size={28} />
                </div>
                <p className="eyebrow">{bridge.bin_id} · PARK LOBBY</p>
                <h2 id="session-title">Link your account</h2>
                <p className="modal-description">
                  Hold your phone near the NFC reader, or use your personal QR code to unlock the tray.
                </p>
                <div className="qr-code" aria-label="Personal QR code">
                  {Array.from({ length: 64 }, (_, index) => (
                    <i
                      key={index}
                      className={(index * 7 + (index % 3)) % 5 < 2 ? "filled" : ""}
                    />
                  ))}
                </div>
                <button
                  className="start-button modal-action"
                  onClick={handleLinkAccount}
                >
                  Simulate NFC link <Icon name="arrow" />
                </button>
              </>
            ) : (
              <div className="linked-state">
                <div
                  className="success-check"
                  style={{
                    backgroundColor: isBlocked
                      ? "rgba(239, 68, 68, 0.15)"
                      : undefined,
                  }}
                >
                  <Icon name={isBlocked ? "close" : "check"} size={32} />
                </div>

                <p className="eyebrow">
                  {bridge.machine_state === "DROPPING"
                    ? "HATCH OPEN · DROPPING ITEMS"
                    : isBlocked
                    ? "LATCH LOCKED · ACTION REQUIRED"
                    : bridge.tray_items.length > 0
                    ? "AI VISION SCAN COMPLETE"
                    : "ACCOUNT LINKED"}
                </p>

                <h2 id="session-title">
                  {bridge.machine_state === "DROPPING"
                    ? "Deposit Confirmed!"
                    : bridge.purity <= 50
                    ? "Liquid Residue Detected!"
                    : bridge.is_anomaly
                    ? "Contamination Alert!"
                    : bridge.tray_items.length > 0
                    ? "Tray Item Checklist"
                    : "Tray unlocked"}
                </h2>

                <p className="modal-description">
                  {bridge.machine_state === "DROPPING"
                    ? "EcoBin hatch is open! Your items are dropping into the chute and rewards are credited to your EcoWallet."
                    : bridge.purity <= 50
                    ? "Bottles contain liquid (Purity ≤ 50%). Bin hatch is locked. Please remove bottles, pour out all liquid, and rescan to claim payout (Est. Payout: RM 0.00)."
                    : bridge.is_anomaly
                    ? "Foreign/Non-recyclable items detected. Bin hatch is locked. Please remove items and rescan."
                    : bridge.tray_items.length > 0
                    ? `Weight: ${bridge.load_cell_weight.toFixed(2)} kg · Purity: ${bridge.purity}% · Est. Payout: RM ${estPayout}`
                    : "Empty your dry recyclables onto the tray. EcoScan will spread, inspect, and weigh each item."}
                </p>

                {/* 1. 尚未检测到垃圾 */}
                {bridge.tray_items.length === 0 && bridge.machine_state !== "DROPPING" && (
                  <div className="live-status">
                    <span className="pulse" />
                    <div>
                      <strong>Waiting for items</strong>
                      <small>Live camera and weight sensors are ready</small>
                    </div>
                  </div>
                )}

                {/* 2. 识别到物品时：展示清单列表 */}
                {bridge.tray_items.length > 0 && (
                  <div style={{ margin: "14px 0", textAlign: "left", display: "flex", flexDirection: "column", gap: "8px" }}>
                    {bridge.tray_items.map((item, i) => {
                      const itemValid = item.ok && !isBlocked
                      return (
                        <div
                          key={i}
                          style={{
                            padding: "10px 12px",
                            borderRadius: "10px",
                            background: itemValid ? "rgba(16, 185, 129, 0.12)" : "rgba(239, 68, 68, 0.14)",
                            border: `1px solid ${itemValid ? "#10B981" : "#EF4444"}`,
                            display: "flex",
                            justifyContent: "space-between",
                            alignItems: "center",
                            fontSize: "0.88rem",
                          }}
                        >
                          <strong style={{ color: itemValid ? "#065F46" : "#991B1B" }}>
                            {itemValid ? "✓ " : "✕ "} {item.name}
                          </strong>
                          <span style={{ fontSize: "0.78rem", opacity: 0.85 }}>
                            {item.status} ({item.confidence})
                          </span>
                        </div>
                      )
                    })}
                  </div>
                )}

                {/* 3. Purity > 50% 且无异常时，显示正常确认开桶按钮 */}
                {bridge.tray_items.length > 0 && !isBlocked && bridge.machine_state !== "DROPPING" && (
                  <button
                    className="start-button modal-action"
                    onClick={handleConfirmDeposit}
                    disabled={confirming}
                    style={{ marginBottom: "8px" }}
                  >
                    <Icon name="check" />
                    {confirming ? "Opening Bin Hatch..." : `Confirm Deposit (+ RM ${estPayout})`}
                  </button>
                )}

                {/* 4. Purity <= 50 或有异常时，显示倒水/复位提示按钮 */}
                {isBlocked && bridge.machine_state !== "DROPPING" && bridge.tray_items.length > 0 && (
                  <button
                    className="withdraw-button modal-action"
                    onClick={handleResetTray}
                    style={{
                      marginBottom: "8px",
                      borderColor: "#F59E0B",
                      color: "#D97706",
                      backgroundColor: "rgba(245, 158, 11, 0.1)",
                      fontWeight: "bold",
                    }}
                  >
                    💧 Liquid / Anomaly Removed · Pour Out & Rescan
                  </button>
                )}

                <button
                  className="withdraw-button modal-action"
                  onClick={() => setSessionOpen(false)}
                >
                  Done
                </button>
              </div>
            )}
          </section>
        </div>
      )}
    </div>
  )
}

export default App