import React from 'react';

export const metadata = {
  title: 'Quorum-Zeolite: Multiscale Physics Engine for Radionuclide Co-Capture',
  description: 'Dual-ion Cs+/Sr2+ co-capture screening for radioactive nuclear wastewater remediation',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body style={{ margin: 0, padding: 0, backgroundColor: '#0a0e17', color: '#f1f5f9' }}>
        {children}
      </body>
    </html>
  );
}
