import { prisma } from '@/lib/prisma';
import { NextRequest, NextResponse } from 'next/server';

// GET /api/audit/[id] - Get audit details
export async function GET(
    request: NextRequest,
    { params }: { params: { id: string } }
) {
    try {
        const audit = await prisma.audit.findUnique({
            where: { id: params.id },
            include: {
                contract: true,
                vulnerabilities: {
                    orderBy: { severity: 'asc' }
                }
            }
        });

        if (!audit) {
            return NextResponse.json(
                { error: 'Audit not found' },
                { status: 404 }
            );
        }

        return NextResponse.json(audit);
    } catch (error) {
        console.error('Error fetching audit:', error);
        return NextResponse.json(
            { error: 'Failed to fetch audit' },
            { status: 500 }
        );
    }
}

// PUT /api/audit/[id] - Update audit status and results
export async function PUT(
    request: NextRequest,
    { params }: { params: { id: string } }
) {
    try {
        const body = await request.json();
        const { status, score, summary, detailReport, slitherRaw, vulnerabilities } = body;

        // Update audit
        const audit = await prisma.audit.update({
            where: { id: params.id },
            data: {
                status,
                score,
                summary,
                detailReport,
                slitherRaw,
                completedAt: status === 'COMPLETED' ? new Date() : undefined,
            }
        });

        // Create vulnerabilities if provided
        if (vulnerabilities && Array.isArray(vulnerabilities)) {
            // Delete existing vulnerabilities
            await prisma.vulnerability.deleteMany({
                where: { auditId: params.id }
            });

            // Create new vulnerabilities
            await prisma.vulnerability.createMany({
                data: vulnerabilities.map((v: any) => ({
                    auditId: params.id,
                    type: v.type,
                    severity: v.severity,
                    description: v.description,
                    location: v.location,
                    lineNumbers: v.lineNumbers || [],
                    markdown: v.markdown,
                    confidence: v.confidence
                }))
            });
        }

        return NextResponse.json(audit);
    } catch (error) {
        console.error('Error updating audit:', error);
        return NextResponse.json(
            { error: 'Failed to update audit' },
            { status: 500 }
        );
    }
}
