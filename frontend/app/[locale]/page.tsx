import { useTranslations } from 'next-intl';
import { Shield, Activity } from 'lucide-react';
import ScanForm from '@/components/ScanForm';
import Link from 'next/link';

export default function DashboardPage() {
    const t = useTranslations('dashboard');
    const tCommon = useTranslations('common');

    return (
        <main className="min-h-screen bg-black">
            {/* Header */}
            <header className="border-b border-cyan-500/30 bg-gradient-to-r from-black via-gray-900 to-black">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <Shield className="w-10 h-10 text-cyan-400" />
                            <div>
                                <h1 className="text-3xl font-bold text-white">{tCommon('appName')}</h1>
                                <p className="text-sm text-cyan-400">{tCommon('tagline')}</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-2">
                            <Link
                                href="/en"
                                className="px-3 py-1 text-sm text-gray-400 hover:text-white transition-colors"
                            >
                                EN
                            </Link>
                            <span className="text-gray-600">|</span>
                            <Link
                                href="/ja"
                                className="px-3 py-1 text-sm text-gray-400 hover:text-white transition-colors"
                            >
                                日本語
                            </Link>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                {/* Dashboard Title */}
                <div className="mb-8">
                    <div className="flex items-center gap-3 mb-2">
                        <Activity className="w-8 h-8 text-cyan-400" />
                        <h2 className="text-4xl font-bold text-white">{t('title')}</h2>
                    </div>
                    <p className="text-gray-400 text-lg">{t('subtitle')}</p>
                </div>

                {/* Scan Form */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <ScanForm />

                    {/* Info Panel */}
                    <div className="bg-gradient-to-br from-cyan-900/20 to-blue-900/20 border border-cyan-500/30 rounded-lg p-8">
                        <h3 className="text-xl font-bold text-white mb-4">🌌 Zero-G Security</h3>
                        <div className="space-y-3 text-gray-300">
                            <p className="text-sm">
                                MamoruAI treats every line of code as if it's floating in the vacuum of space—where
                                a single vulnerability can eject your entire capital into the void.
                            </p>
                            <ul className="text-sm space-y-2 list-disc list-inside">
                                <li>AI-powered contextual analysis</li>
                                <li>Slither static analysis integration</li>
                                <li>Real-time vulnerability detection</li>
                                <li>Bilingual support (EN/JA)</li>
                            </ul>
                        </div>
                    </div>
                </div>

                {/* Recent Audits Section */}
                <div className="mt-12">
                    <h3 className="text-2xl font-bold text-white mb-6">{t('recentAudits')}</h3>
                    <div className="bg-gray-900/50 border border-gray-700 rounded-lg p-8 text-center">
                        <p className="text-gray-400">No recent audits. Start your first security scan above.</p>
                    </div>
                </div>
            </div>

            {/* Footer */}
            <footer className="border-t border-gray-800 mt-20">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                    <p className="text-center text-gray-500 text-sm">
                        Built with ❤️ for the decentralized future. Stay safe in Zero-G. 🚀
                    </p>
                </div>
            </footer>
        </main>
    );
}
