export const useMessaging = () => {
  const { apiFetch } = useApi();

  const conversations      = useState<any[]>('messaging-conversations',       () => []);
  const currentMessages    = useState<any[]>('messaging-current-messages',    () => []);
  const currentConversation = useState<any>('messaging-current-conversation', () => null);
  const loading            = useState<boolean>('messaging-loading',           () => false);
  const sending            = useState<boolean>('messaging-sending',           () => false);
  const unreadCount        = useState<number>('messaging-unread-count',       () => 0);

  const fetchConversations = async () => {
    loading.value = true;
    try {
      const res = await apiFetch('/api/messaging/conversations/');
      conversations.value = res.results ?? res;
      unreadCount.value = conversations.value.reduce(
        (sum: number, c: any) => sum + (c.unread_count ?? 0), 0
      );
    } catch (err: any) {
      console.error('fetchConversations error:', err);
    } finally {
      loading.value = false;
    }
  };

  const fetchMessages = async (conversationId: string) => {
    loading.value = true;
    try {
      const res = await apiFetch('/api/messaging/messages/', {
        params: { conversation: conversationId },
      });
      currentMessages.value = res.results ?? res;
    } catch (err: any) {
      console.error('fetchMessages error:', err);
    } finally {
      loading.value = false;
    }
  };

  const sendMessage = async (conversationId: string, content: string) => {
    sending.value = true;
    try {
      const msg = await apiFetch('/api/messaging/messages/', {
        method: 'POST',
        body: { conversation: conversationId, content },
      });
      currentMessages.value = [...currentMessages.value, msg];
      // Mettre à jour le last_message de la conversation locale
      const idx = conversations.value.findIndex((c: any) => c.uuid === conversationId);
      if (idx !== -1) {
        conversations.value[idx] = {
          ...conversations.value[idx],
          last_message: { content, created_at: new Date().toISOString() },
        };
      }
      return msg;
    } catch (err: any) {
      console.error('sendMessage error:', err);
      throw err;
    } finally {
      sending.value = false;
    }
  };

  const startConversation = async (otherUserUuid: string, relatedPostId?: number | null) => {
    const body: any = { other_user_uuid: otherUserUuid };
    if (relatedPostId) body.related_post_id = relatedPostId;
    const conv = await apiFetch('/api/messaging/conversations/', {
      method: 'POST',
      body,
    });
    // Ajouter à la liste locale si absent
    const exists = conversations.value.some((c: any) => c.uuid === conv.uuid);
    if (!exists) conversations.value = [conv, ...conversations.value];
    currentConversation.value = conv;
    return conv;
  };

  const markAsRead = async (conversationId: string) => {
    try {
      await apiFetch('/api/messaging/messages/mark-as-read/', {
        method: 'POST',
        body: { conversation: conversationId },
      });
      // Mettre à jour le compteur local
      const idx = conversations.value.findIndex((c: any) => c.uuid === conversationId);
      if (idx !== -1) {
        const prev = conversations.value[idx].unread_count ?? 0;
        conversations.value[idx] = { ...conversations.value[idx], unread_count: 0 };
        unreadCount.value = Math.max(0, unreadCount.value - prev);
      }
    } catch (err: any) {
      console.error('markAsRead error:', err);
    }
  };

  const clearMessagingState = () => {
    conversations.value       = [];
    currentMessages.value     = [];
    currentConversation.value = null;
    unreadCount.value         = 0;
  };

  return {
    conversations,
    currentMessages,
    currentConversation,
    loading,
    sending,
    unreadCount,
    fetchConversations,
    fetchMessages,
    sendMessage,
    startConversation,
    markAsRead,
    clearMessagingState,
  };
};
