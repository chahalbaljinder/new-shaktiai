'use client'

import { motion } from 'framer-motion'
import { 
  TrendingUp, 
  TrendingDown, 
  Users, 
  FileText, 
  CheckCircle, 
  Clock,
  Eye,
  ShoppingCart,
  DollarSign,
  ArrowUp,
  ArrowDown
} from 'lucide-react'
import { useAppStore } from '@/lib/store'

interface DashboardProps {
  userName?: string
}

const statsData = [
  {
    title: 'DRDO Personnel',
    value: '1,247',
    change: '+15.3%',
    isPositive: true,
    icon: Users,
    iconBg: 'bg-[#3C50E0]',
    iconColor: 'text-white'
  },
  {
    title: 'Policy Queries',
    value: '8,592',
    change: '+23.8%',
    isPositive: true,
    icon: FileText,
    iconBg: 'bg-[#10B981]',
    iconColor: 'text-white'
  },
  {
    title: 'Active Sessions',
    value: '342',
    change: '+8.7%',
    isPositive: true,
    icon: CheckCircle,
    iconBg: 'bg-[#F59E0B]',
    iconColor: 'text-white'
  },
  {
    title: 'APEX Agents',
    value: '12',
    change: 'All Active',
    isPositive: true,
    icon: Clock,
    iconBg: 'bg-[#EF4444]',
    iconColor: 'text-white'
  }
]

const recentOrders = [
  {
    id: 'QRY-089',
    product: 'POSH Policy - Sexual Harassment Guidelines',
    status: 'Completed',
    amount: '2m 15s',
    statusColor: 'text-[#10B981] bg-[#10B981]/10'
  },
  {
    id: 'QRY-088',
    product: 'Maternity Leave - DRDO Entitlements',
    status: 'Processing',
    amount: '1m 42s',
    statusColor: 'text-[#F59E0B] bg-[#F59E0B]/10'
  },
  {
    id: 'QRY-087',
    product: 'Annual Performance Review - Scientists',
    status: 'Completed',
    amount: '3m 08s',
    statusColor: 'text-[#10B981] bg-[#10B981]/10'
  },
  {
    id: 'QRY-086',
    product: 'Grade Pay & Allowances Structure',
    status: 'Completed',
    amount: '1m 55s',
    statusColor: 'text-[#10B981] bg-[#10B981]/10'
  },
  {
    id: 'QRY-085',
    product: 'Leave Policy - Casual & Medical',
    status: 'Completed',
    amount: '2m 30s',
    statusColor: 'text-[#10B981] bg-[#10B981]/10'
  }
]

const customerDemographic = [
  { country: 'Delhi HQ', customers: 423, percentage: 34, flag: '🏛️' },
  { country: 'Bangalore Labs', customers: 356, percentage: 29, flag: '🔬' },
  { country: 'Hyderabad Labs', customers: 287, percentage: 23, flag: '⚙️' },
  { country: 'Other Establishments', customers: 181, percentage: 14, flag: '📍' }
]

export default function Dashboard({ userName = 'User' }: DashboardProps) {
  const { setCurrentPage } = useAppStore()

  return (
    <div className="min-h-screen">
      <div className="max-w-[1600px] mx-auto space-y-6">
        {/* Page Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-[#1C2434] dark:text-white">
              DRDO APEX Dashboard
            </h1>
            <p className="text-[#64748B] mt-1">
              Welcome, {userName}! AI-Powered Expert System for DRDO Personnel
            </p>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 lg:gap-6">
          {statsData.map((stat, index) => (
            <motion.div
              key={stat.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white dark:bg-[#24303F] rounded-lg border border-[#E2E8F0] dark:border-[#313D4F] p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-[#64748B] text-sm font-medium mb-1">
                    {stat.title}
                  </h3>
                  <p className="text-2xl font-bold text-[#1C2434] dark:text-white">
                    {stat.value}
                  </p>
                  <div className="flex items-center mt-2">
                    {stat.isPositive ? (
                      <ArrowUp size={16} className="text-[#10B981]" />
                    ) : (
                      <ArrowDown size={16} className="text-[#EF4444]" />
                    )}
                    <span className={`text-sm font-medium ml-1 ${
                      stat.isPositive ? 'text-[#10B981]' : 'text-[#EF4444]'
                    }`}>
                      {stat.change}
                    </span>
                  </div>
                </div>
                <div className={`${stat.iconBg} p-3 rounded-full`}>
                  <stat.icon size={24} className={stat.iconColor} />
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Charts & Tables Section */}
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-4 lg:gap-6">
          {/* Recent Orders Table */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-white dark:bg-[#24303F] rounded-lg border border-[#E2E8F0] dark:border-[#313D4F] overflow-hidden"
          >
            <div className="p-6 border-b border-[#E2E8F0] dark:border-[#313D4F]">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-bold text-[#1C2434] dark:text-white">
                  Recent Policy Queries
                </h2>
                <button className="text-sm text-[#3C50E0] hover:underline font-medium">
                  View all queries
                </button>
              </div>
            </div>
            
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-[#F9FAFB] dark:bg-[#1C2434]">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-[#64748B] uppercase tracking-wider">
                      Query
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-[#64748B] uppercase tracking-wider">
                      Response Time
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-[#64748B] uppercase tracking-wider">
                      Status
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#E2E8F0] dark:divide-[#313D4F]">
                  {recentOrders.map((order) => (
                    <tr key={order.id} className="hover:bg-[#F9FAFB] dark:hover:bg-[#1C2434] transition-colors">
                      <td className="px-6 py-4">
                        <div>
                          <div className="text-sm font-medium text-[#1C2434] dark:text-white">
                            {order.product}
                          </div>
                          <div className="text-xs text-[#64748B]">{order.id}</div>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-sm text-[#1C2434] dark:text-white font-medium">
                        {order.amount}
                      </td>
                      <td className="px-6 py-4">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${order.statusColor}`}>
                          {order.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </motion.div>

          {/* Customer Demographics */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="bg-white dark:bg-[#24303F] rounded-lg border border-[#E2E8F0] dark:border-[#313D4F] p-6"
          >
            <h2 className="text-lg font-bold text-[#1C2434] dark:text-white mb-6">
              Personnel Distribution
            </h2>
            <p className="text-sm text-[#64748B] mb-6">
              Active DRDO personnel across establishments
            </p>
            
            <div className="space-y-4">
              {customerDemographic.map((item) => (
                <div key={item.country}>
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      <span className="text-2xl">{item.flag}</span>
                      <span className="text-sm font-medium text-[#1C2434] dark:text-white">
                        {item.country}
                      </span>
                    </div>
                    <span className="text-sm font-semibold text-[#1C2434] dark:text-white">
                      {item.customers} Personnel
                    </span>
                  </div>
                  <div className="w-full bg-[#E2E8F0] dark:bg-[#313D4F] rounded-full h-2">
                    <div 
                      className="bg-[#3C50E0] h-2 rounded-full transition-all duration-300"
                      style={{ width: `${item.percentage}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Agent Activity Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="bg-white dark:bg-[#24303F] rounded-lg border border-[#E2E8F0] dark:border-[#313D4F] p-6"
        >
          <h2 className="text-lg font-bold text-[#1C2434] dark:text-white mb-2">
            APEX Agent Performance
          </h2>
          <p className="text-sm text-[#64748B] mb-6">
            Real-time performance metrics of DRDO APEX AI agents
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm text-[#64748B]">Success Rate</span>
                <span className="text-sm font-bold text-[#1C2434] dark:text-white">94.3%</span>
              </div>
              <div className="w-full bg-[#E2E8F0] dark:bg-[#313D4F] rounded-full h-2">
                <div className="bg-[#3C50E0] h-2 rounded-full" style={{ width: '94%' }} />
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm text-[#64748B]">Avg Response Time</span>
                <span className="text-sm font-bold text-[#1C2434] dark:text-white">2.3s</span>
              </div>
              <div className="w-full bg-[#E2E8F0] dark:bg-[#313D4F] rounded-full h-2">
                <div className="bg-[#10B981] h-2 rounded-full" style={{ width: '85%' }} />
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm text-[#64748B]">User Satisfaction</span>
                <span className="text-sm font-bold text-[#1C2434] dark:text-white">4.7/5</span>
              </div>
              <div className="w-full bg-[#E2E8F0] dark:bg-[#313D4F] rounded-full h-2">
                <div className="bg-[#F59E0B] h-2 rounded-full" style={{ width: '94%' }} />
              </div>
            </div>
          </div>
          
          <div className="mt-6 p-4 bg-[#F9FAFB] dark:bg-[#1C2434] rounded-lg">
            <div className="flex items-center space-x-2">
              <TrendingUp className="text-[#10B981]" size={20} />
              <p className="text-sm text-[#64748B]">
                APEX agents handled <span className="font-semibold text-[#1C2434] dark:text-white">342 policy queries</span> today, 
                up 18% from yesterday. System operating at optimal efficiency!
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}
