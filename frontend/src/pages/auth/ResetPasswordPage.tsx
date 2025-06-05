'use client'

import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Loader2 } from 'lucide-react'
import axios from 'axios'

type Status = 'loading' | 'valid' | 'invalid' | 'submitting' | 'success'

export function ResetPasswordPage() {
  const [URLSearchParams,] = useSearchParams()
  const token = URLSearchParams.get('token')
  const [status, setStatus] = useState<Status>('loading')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    const verifyToken = async () => {
      try {
        const res = await axios.get(`/api/auth/verify-reset-token?token=${token}`)
        if (res.data.valid) {
          setStatus('valid')
        } else {
          setStatus('invalid')
        }
      } catch (err) {
        setStatus('invalid')
      }
    }

    if (token) {
      verifyToken()
    } else {
      setStatus('invalid')
    }
  }, [token])

  const handleReset = async (e: React.FormEvent) => {
    e.preventDefault()

    if (newPassword !== confirmPassword) {
      setError('Passwords do not match.')
      return
    }

    try {
      setStatus('submitting')
      await axios.post('/api/auth/reset-password', {
        token,
        new_password: newPassword,
      })
      setStatus('success')
    } catch (err) {
      setError('Failed to reset password. Try again.')
      setStatus('valid') // Go back to form
    }
  }

  if (status === 'loading') {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="mr-2 h-6 w-6 animate-spin" />
        Verifying reset link...
      </div>
    )
  }

  if (status === 'invalid') {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Alert variant="destructive">
          <AlertTitle>Invalid or Expired Link</AlertTitle>
          <AlertDescription>
            This password reset link is no longer valid. Please request a new one.
          </AlertDescription>
        </Alert>
      </div>
    )
  }

  if (status === 'success') {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Alert variant="default">
          <AlertTitle>Password Reset Successful</AlertTitle>
          <AlertDescription>
            You can now log in with your new password.
          </AlertDescription>
        </Alert>
      </div>
    )
  }

  return (
    <div className="flex items-center justify-center min-h-screen">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Reset Your Password</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleReset} className="space-y-4">
            <div>
              <Label htmlFor="new-password">New Password</Label>
              <Input
                id="new-password"
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                required
              />
            </div>
            <div>
              <Label htmlFor="confirm-password">Confirm New Password</Label>
              <Input
                id="confirm-password"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
            </div>
            {error && <p className="text-sm text-red-600">{error}</p>}
            <Button type="submit" className="w-full" disabled={status === 'submitting'}>
              {status === 'submitting' && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Reset Password
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
