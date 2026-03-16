'use client';

import { useTranslations } from 'next-intl';
import { Shield, AlertTriangle, CheckCircle, Clock, XCircle } from 'lucide-react';

interface SecurityScoreProps {
    score: number;
    status?: string;
}

export default function SecurityScore({ score, status }: SecurityScoreProps) {
    const t = useTranslations('audit');

    const getScoreColor = (score: number) => {
        if (score >= 80) return 'text-green-400';
        if (score >= 60) return 'text-yellow-400';
        if (score >= 40) return 'text-orange-400';
        return 'text-red-400';
    };

    const getScoreGradient = (score: number) => {
        if (score >= 80) return 'from-green-500 to-emerald-600';
        if (score >= 60) return 'from-yellow-500 to-orange-500';
        if (score >= 40) return 'from-orange-500 to-red-500';
        return 'from-red-500 to-rose-600';
    };

    const circumference = 2 * Math.PI * 70;
    const strokeDashoffset = circumference - (score / 100) * circumference;

    return (
        <div className="flex flex-col items-center justify-center p-8">
            <div className="relative w-48 h-48">
                <svg className="transform -rotate-90 w-48 h-48">
                    <circle
                        cx="96"
                        cy="96"
                        r="70"
                        stroke="currentColor"
                        strokeWidth="12"
                        fill="transparent"
                        className="text-gray-800"
                    />
                    <circle
                        cx="96"
                        cy="96"
                        r="70"
                        stroke="currentColor"
                        strokeWidth="12"
                        fill="transparent"
                        strokeDasharray={circumference}
                        strokeDashoffset={strokeDashoffset}
                        className={`${getScoreColor(score)} transition-all duration-1000 ease-out`}
                        strokeLinecap="round"
                    />
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className={`text-5xl font-bold ${getScoreColor(score)}`}>
                        {score}
                    </span>
                    <span className="text-sm text-gray-400 mt-1">/ 100</span>
                </div>
            </div>
            <p className="text-lg font-semibold text-gray-300 mt-4">{t('score')}</p>
        </div>
    );
}
