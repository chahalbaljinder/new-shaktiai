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
    title: 'Total Queries',
    value: '3,782',
    change: '+11.01%',
    isPositive: true,
    icon: Users,
    iconBg: 'bg-[#3C50E0]',
    iconColor: 'text-white'
  },
  {
    title: 'Active Cases',
    value: '5,359',
    change: '+9.05%',
    isPositive: true,
    icon: FileText,
    iconBg: 'bg-[#10B981]',
    iconColor: 'text-white'
  },
  {
    title: 'Resolved',
    value: '2,450',
    change: '+2.59%',
    isPositive: true,
    icon: CheckCircle,
    iconBg: 'bg-[#F59E0B]',
    iconColor: 'text-white'
  },
  {
    title: 'Pending',
    value: '1,289',
    change: '-0.95%',
    isPositive: false,
    icon: Clock,
    iconBg: 'bg-[#EF4444]',
    iconColor: 'text-white'
  }
]

const recentOrders = [
  {
    id: 'ORD-001',
    product: 'Query: POSH Policy',
    status: 'Delivered',
    amount: '$2399.00',
    statusColor: 'text-[#10B981] bg-[#10B981]/10'
  },
  {
    id: 'ORD-002',
    product: 'Complaint: Workplace Issue',
    status: 'Pending',
    amount: '$879.00',
    statusColor: 'text-[#F59E0B] bg-[#F59E0B]/10'
  },
  {
    id: 'ORD-003',
    product: 'Feedback: Annual Review',
    status: 'Delivered',
    amount: '$1869.00',
    statusColor: 'text-[#10B981] bg-[#10B981]/10'
  },
  {
    id: 'ORD-004',
    product: 'Query: Leave Policy',
    status: 'Canceled',
    amount: '$1699.00',
    statusColor: 'text-[#EF4444] bg-[#EF4444]/10'
  },
  {
    id: 'ORD-005',
    product: 'Support: HR Escalation',
    status: 'Delivered',
    amount: '$240.00',
    statusColor: 'text-[#10B981] bg-[#10B981]/10'
  }
]

const customerDemographic = [
  { country: 'USA', customers: 2379, percentage: 79, flag: '🇺🇸' },
  { country: 'India', customers: 1589, percentage: 53, flag: '🇮🇳' },
  { country: 'UK', customers: 989, percentage: 33, flag: '🇬🇧' },
  { country: 'Germany', customers: 589, percentage: 20, flag: '🇩🇪' }
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
              Dashboard
            </h1>
            <p className="text-[#64748B] mt-1">
              Welcome back, {userName}! Here's what's happening today.
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
                  Recent Orders
                </h2>
                <button className="text-sm text-[#3C50E0] hover:underline font-medium">
                  See all
                </button>
              </div>
            </div>
            
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-[#F9FAFB] dark:bg-[#1C2434]">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-[#64748B] uppercase tracking-wider">
                      Product
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-[#64748B] uppercase tracking-wider">
                      Amount
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
              Customers Demographic
            </h2>
            <p className="text-sm text-[#64748B] mb-6">
              Number of customers based on country
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
                      {item.customers} Customers
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

        {/* Monthly Target Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="bg-white dark:bg-[#24303F] rounded-lg border border-[#E2E8F0] dark:border-[#313D4F] p-6"
        >
          <h2 className="text-lg font-bold text-[#1C2434] dark:text-white mb-2">
            Monthly Target
          </h2>
          <p className="text-sm text-[#64748B] mb-6">
            Target you've set for each month
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm text-[#64748B]">Target</span>
                <span className="text-sm font-bold text-[#1C2434] dark:text-white">$20K</span>
              </div>
              <div className="w-full bg-[#E2E8F0] dark:bg-[#313D4F] rounded-full h-2">
                <div className="bg-[#3C50E0] h-2 rounded-full" style={{ width: '75%' }} />
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm text-[#64748B]">Revenue</span>
                <span className="text-sm font-bold text-[#1C2434] dark:text-white">$15K</span>
              </div>
              <div className="w-full bg-[#E2E8F0] dark:bg-[#313D4F] rounded-full h-2">
                <div className="bg-[#10B981] h-2 rounded-full" style={{ width: '60%' }} />
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm text-[#64748B]">Today</span>
                <span className="text-sm font-bold text-[#1C2434] dark:text-white">$3.2K</span>
              </div>
              <div className="w-full bg-[#E2E8F0] dark:bg-[#313D4F] rounded-full h-2">
                <div className="bg-[#F59E0B] h-2 rounded-full" style={{ width: '45%' }} />
              </div>
            </div>
          </div>
          
          <div className="mt-6 p-4 bg-[#F9FAFB] dark:bg-[#1C2434] rounded-lg">
            <div className="flex items-center space-x-2">
              <TrendingUp className="text-[#10B981]" size={20} />
              <p className="text-sm text-[#64748B]">
                You earn <span className="font-semibold text-[#1C2434] dark:text-white">$3287</span> today, 
                it's higher than last month. Keep up your good work!
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}
