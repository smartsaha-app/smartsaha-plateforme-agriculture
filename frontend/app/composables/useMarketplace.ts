import { computed } from 'vue';

export const useMarketplace = () => {
  const { apiFetch } = useApi();

  // ── État global partagé (clés statiques obligatoires pour useState Nuxt) ──────
  const products    = useState<any[]>('marketplace-products', () => []);
  const categories  = useState<any[]>('marketplace-categories', () => []);
  const cart        = useState<any>('marketplace-cart', () => null);
  const orders      = useState<any[]>('marketplace-orders', () => []);
  const orderDetail = useState<any>('marketplace-order-detail', () => null);
  const transactions = useState<any[]>('marketplace-transactions', () => []);
  const loading     = useState<boolean>('marketplace-loading', () => false);
  const error       = useState<string | null>('marketplace-error', () => null);

  // ── Badge panier (utilisé dans le header) ────────────────────────────────────
  const cartItemCount = computed<number>(() => cart.value?.items_count ?? 0);

  // ── Réinitialisation à la déconnexion (isolation entre utilisateurs) ─────────
  const clearMarketplaceState = () => {
    products.value    = [];
    cart.value        = null;
    orders.value      = [];
    orderDetail.value = null;
    transactions.value = [];
    error.value       = null;
  };

  // ── Produits (catalogue public — uniquement les produits actifs côté buyer) ──
  const fetchProducts = async (params: Record<string, any> = {}) => {
    loading.value = true;
    try {
      const response = await apiFetch('/api/catalogue/products/', { params });
      products.value = response.results || response;
    } catch (err: any) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await apiFetch('/api/catalogue/categories/');
      categories.value = response.results || response;
    } catch (err: any) {
      console.error('Error fetching categories:', err);
    }
  };

  // ── Panier (filtré côté backend par request.user via cookie JWT) ─────────────
  const fetchCart = async () => {
    try {
      const response = await apiFetch('/api/orders/cart/');
      cart.value = Array.isArray(response) ? response[0] : response;
    } catch (err: any) {
      console.error('Error fetching cart:', err);
    }
  };

  const addToCart = async (productId: number, quantity: number = 1) => {
    const response = await apiFetch('/api/orders/cart/add_item/', {
      method: 'POST',
      body: { product_id: productId, quantity },
    });
    cart.value = response;
    return response;
  };

  const removeFromCart = async (itemId: number) => {
    const response = await apiFetch('/api/orders/cart/remove_item/', {
      method: 'POST',
      body: { item_id: itemId },
    });
    cart.value = response;
    return response;
  };

  const checkout = async (deliveryData: any) => {
    const response = await apiFetch('/api/orders/cart/checkout/', {
      method: 'POST',
      body: deliveryData,
    });
    cart.value = null;
    await fetchOrders();
    return response;
  };

  // ── Commandes (filtrées côté backend par buyer=request.user) ─────────────────
  const fetchOrders = async (params: Record<string, any> = {}) => {
    loading.value = true;
    try {
      const response = await apiFetch('/api/orders/orders/', { params });
      orders.value = response.results || response;
    } catch (err: any) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  };

  const fetchOrderDetail = async (id: string | number) => {
    loading.value = true;
    try {
      const response = await apiFetch(`/api/orders/orders/${id}/`);
      orderDetail.value = response;
    } catch (err: any) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  };

  const initiatePayment = async (paymentData: { order_id: number, method: string, phone?: string, payment_token?: string }) => {
    loading.value = true;
    try {
      const response = await apiFetch('/api/mobile/payments/initiate/', {
        method: 'POST',
        body: paymentData,
      });
      return response;
    } catch (err: any) {
      error.value = err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const fetchTransactions = async () => {
    loading.value = true;
    try {
      const response = await apiFetch('/api/mobile/payments/history/');
      transactions.value = response.results || response;
    } catch (err: any) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  };

  const updateOrderStatus = async (orderId: string | number, status: string) => {
    loading.value = true;
    try {
      const response = await apiFetch(`/api/orders/orders/${orderId}/update-status/`, {
        method: 'POST',
        body: { status }
      });
      // Mettre à jour l'état local si nécessaire
      if (orderDetail.value && orderDetail.value.id === orderId) {
        orderDetail.value = response;
      }
      return response;
    } catch (err: any) {
      error.value = err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const sellerStats = ref({ available_balance: 0, escrow_balance: 0, total_sales: 0 });

  const fetchSellerStats = async () => {
    loading.value = true;
    try {
      const response = await apiFetch('/api/mobile/payments/seller-stats/');
      sellerStats.value = response;
    } catch (err: any) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  };

  return {
    // State
    products,
    categories,
    cart,
    orders,
    orderDetail,
    transactions,
    sellerStats,
    loading,
    error,
    cartItemCount,
    // Actions
    fetchProducts,
    fetchCategories,
    fetchCart,
    addToCart,
    removeFromCart,
    checkout,
    fetchOrders,
    fetchOrderDetail,
    initiatePayment,
    fetchTransactions,
    updateOrderStatus,
    fetchSellerStats,
    clearMarketplaceState,
  };
};
