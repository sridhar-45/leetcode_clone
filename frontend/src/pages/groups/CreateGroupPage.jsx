import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { groupsAPI } from '../../services/groupsAPI'
import Button from '../../components/common/Button'
import toast from 'react-hot-toast'

const CreateGroupPage = () => {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    is_public: true,
    max_members: 50,
  })

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    try {
      setLoading(true)
      const group = await groupsAPI.createGroup(formData)
      toast.success('Group created successfully!')
      navigate(`/groups/${group.slug}`)
    } catch (error) {
      toast.error(error.response?.data?.error || 'Failed to create group')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 py-8">
      <div className="max-w-2xl mx-auto px-4">
        <h1 className="text-3xl font-bold text-white mb-8">Create Group</h1>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-2">Group Name *</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded text-white"
                  placeholder="Code Warriors"
                />
              </div>

              <div>
                <label className="block text-sm text-gray-400 mb-2">Description</label>
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  rows={4}
                  className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded text-white"
                  placeholder="Tell others about your group..."
                />
              </div>

              <div>
                <label className="block text-sm text-gray-400 mb-2">Max Members</label>
                <input
                  type="number"
                  name="max_members"
                  value={formData.max_members}
                  onChange={handleChange}
                  min="2"
                  max="100"
                  className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded text-white"
                />
              </div>

              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  name="is_public"
                  checked={formData.is_public}
                  onChange={handleChange}
                  className="w-4 h-4"
                />
                <label className="text-sm text-gray-400">
                  Public group (anyone can join)
                </label>
              </div>
            </div>
          </div>

          <div className="flex items-center justify-end gap-4">
            <button
              type="button"
              onClick={() => navigate('/groups')}
              className="px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition"
            >
              Cancel
            </button>
            <Button type="submit" variant="success" size="large" loading={loading}>
              Create Group
            </Button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default CreateGroupPage